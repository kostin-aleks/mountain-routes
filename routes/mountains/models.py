""" mountains models """

import math
import os
import re
import random
from slugify import slugify

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse

from faker import Faker
from routes.utils import get_image_path


def thumbnail(width, height):
    """ thumbnail """
    max_ = 400
    factor = width / height
    if height > max_:
        height = max_
        width = int(height * factor)
    return {'width': width, 'height': height}


def slugify_name(cls, name):
    """
    slugify name and check unique value
    """
    slug = slugify(name, to_lower=True)
    while cls.objects.filter(slug=slug).count():
        slug += '-1'
    return slug


class GeoPoint(models.Model):
    """
    GeoPoint stores data related to point on Earth surface
    """
    latitude = models.DecimalField(
        _("latitude"), default=0, decimal_places=6, max_digits=10)
    longitude = models.DecimalField(
        _("longitude"), default=0, decimal_places=6, max_digits=10)

    def __str__(self):
        return f'point {self.latitude:10.6f}, {self.longitude:10.4f}'

    class Meta:
        db_table = 'geopoint'
        verbose_name = _("geopoint")
        verbose_name_plural = _("geopoints")

    def distance_to_point(self, point):
        """
        distance from this point to another point, km
        """
        if point is not None:
            return haversine_distance(
                self.latitude, self.longitude, point.latitude, point.longitude)
        return None

    def distance_to_coordinates(self, latitude, longitude):
        """
        distance from this point to point given by coordinates, km
        """
        return haversine_distance(
            self.latitude, self.longitude, latitude, longitude)

    @classmethod
    def degree_from_string(cls, string):
        """ get degree from string """
        items = [float(x) for x in string.split()]
        return items[0] + items[1] / 60.0 + items[2] / 3600.0

    @classmethod
    def coordinate_from_string(cls, string):
        """
        get degree from string that contains digits and other symbols
        """
        items = list(map(int, re.findall(r'\d+', string)))
        if items:
            degree = items[0] + items[1] / 60.0 + items[2] / 3600.0
            if 'W' in string or 'S' in string or 'ю.ш.' in string or 'з.д.' in string:
                degree = -degree
            return degree
        return None

    def field_value(self, name='lat'):
        """
        return latitude or longitude
        """
        return self.longitude if name == 'lon' else self.latitude

    def degrees(self, name):
        """
        return coordinate degrees as integer value
        """
        value = self.field_value(name)
        return int(value)

    def minutes(self, name):
        """
        return coordinate minutes as integer value
        """
        value = float(self.field_value(name))
        return int((value - self.degrees(name)) * 60.0)

    def seconds(self, name):
        """
        return coordinate seconds as integer value
        """
        value = float(self.field_value(name))
        return int(round((value - self.degrees(name) - self.minutes(name) / 60.0) * 3600.0))


class Ridge(models.Model):
    """
    Ridge model
    """
    slug = models.SlugField(_("slug"), max_length=128, unique=True)
    name = models.CharField(_("name"), max_length=128)
    description = models.TextField(_("description"), blank=True, null=True)
    editor = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, verbose_name=_("editor"), null=True)
    changed = models.DateTimeField(
        _("created"), default=timezone.now, db_index=True)

    class Meta:
        db_table = 'ridge'
        verbose_name = _("ridge")
        verbose_name_plural = _("ridges")

    def __str__(self):
        return f'{self.id}-{self.slug}'

    def get_absolute_url(self):
        """
        get absolute url to the ridge
        """
        return reverse("ridge", kwargs={"slug": self.slug})

    def peaks(self):
        """ ridge peaks """
        return self.peak_set.order_by('name')

    def links(self):
        """ ridge links """
        return self.ridgeinfolink_set.order_by('id')

    def routes(self):
        """ ridge routes """
        return Route.objects.filter(peak__ridge=self).order_by('number')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_name(Ridge, self.name)
        return super().save(*args, **kwargs)

    def can_be_edited(self, user):
        """
        can the user edit this ridge
        """
        if user is None:
            return False
        if user.is_anonymous:
            return False
        if user.is_superuser:
            return True
        climber = user.climber
        if climber.is_editor and self.editor == user:
            return True
        return False

    def can_be_removed(self):
        """
        can be removed this ridge ?
        """
        return self.peak_set.all().count() == 0


class RidgeInfoLink(models.Model):
    """
    Ridge Info Link model
    """
    ridge = models.ForeignKey(
        Ridge, on_delete=models.PROTECT, verbose_name=_("ridge"))
    link = models.URLField(_("link"), max_length=128)
    description = models.CharField(
        _("description"), max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'ridge_info_link'
        verbose_name = _("ridge link")
        verbose_name_plural = _("ridge links")

    def __str__(self):
        return f'{self.id}-{self.link}'


class Peak(models.Model):
    """
    Peak model
    """
    slug = models.SlugField(_("slug"), max_length=64, unique=True)
    ridge = models.ForeignKey(
        Ridge, on_delete=models.PROTECT, verbose_name=_("ridge"))
    name = models.CharField(_("name"), max_length=64, blank=True, null=True)
    height = models.IntegerField(_("height"), blank=True, null=True, default=0)
    description = models.TextField(_("description"), blank=True, null=True)
    photo = models.ImageField(
        _("photo"), upload_to=get_image_path, blank=True, null=True)
    point = models.ForeignKey(
        GeoPoint, blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name=_("point"))
    editor = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, verbose_name=_("editor"), null=True)
    changed = models.DateTimeField(
        _("created"), default=timezone.now, db_index=True)

    class Meta:
        db_table = 'peak'
        verbose_name = _("peak")
        verbose_name_plural = _("peaks")

    def __str__(self):
        return f'{self.id}-{self.slug}'

    def routes(self):
        """ peak routes """
        return self.route_set.order_by('number')

    def photos(self):
        """ peak photos """
        return self.peakphoto_set.order_by('id')

    def comments(self):
        """
        peak comments only
        no replies
        """
        return self.peakcomment_set.filter(
            active=True).filter(parent__isnull=True).order_by('id')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_name(Peak, self.name)
        return super().save(*args, **kwargs)

    def can_be_edited(self, user):
        """
        can the user edit this peak
        """
        if user is None:
            return False
        if user.is_anonymous:
            return False
        if user.is_superuser:
            return True
        climber = user.climber
        if climber.is_editor and self.editor == user:
            return True
        return False

    def can_be_removed(self):
        """
        can be removed this peak ?
        """
        return self.route_set.all().count() == 0


class PeakPhoto(models.Model):
    """
    Peak Photo model
    """
    peak = models.ForeignKey(
        Peak, on_delete=models.PROTECT, verbose_name=_("peak"))
    photo = models.ImageField(
        _("photo"), upload_to=get_image_path, blank=True, null=True)
    description = models.CharField(_("description"), max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'peak_photo'
        verbose_name = _("peak photo")
        verbose_name_plural = _("peak photos")

    def __str__(self):
        return f'{self.id}-{self.photo}'

    @property
    def thumbnail(self):
        """ get photo thumbnail """
        return thumbnail(self.photo.width, self.photo.height)


class PeakComment(models.Model):
    """
    Peak Comment model
    """
    peak = models.ForeignKey(Peak, verbose_name=_("peak"),
                             on_delete=models.CASCADE)
    parent = models.ForeignKey("PeakComment", verbose_name=_("parent"),
                               null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT,
        verbose_name=_("author"), null=True)
    nickname = models.CharField(_("nickname"), max_length=80, null=True)
    email = models.EmailField(_("email"), null=True)
    homepage = models.URLField(_("home page"), max_length=200, blank=True, null=True)
    body = models.TextField(_("body"))
    photo = models.ImageField(
        _("photo"), upload_to=get_image_path, blank=True, null=True)
    doc = models.FileField(
        _("doc"), upload_to=get_image_path, blank=True, null=True)
    ip_address = models.GenericIPAddressField(_("IP address"), blank=True, null=True)
    country_code = models.CharField(_("country code"), max_length=16, null=True)
    country = models.CharField(_("country"), max_length=255, null=True)
    region = models.CharField(_("region"), max_length=255, null=True)
    city = models.CharField(_("city"), max_length=255, null=True)
    created_on = models.DateTimeField(_("created"), auto_now_add=True)
    active = models.BooleanField(_("active"), default=True)

    class Meta:
        ordering = ['created_on']
        db_table = 'peak_comment'
        verbose_name = _("peak comment")
        verbose_name_plural = _("peak comments")

    def __str__(self):
        return f'comment {self.id} by {self.name}'

    @property
    def name(self):
        """ get author name """
        return self.author.username if self.author else self.nickname

    @property
    def replies(self):
        """ get replies for the this comment """
        return PeakComment.objects.filter(
            parent=self).filter(active=True).order_by('id')

    @property
    def doc_name(self):
        """ get doc's file name """
        return os.path.basename(self.doc.name)

    @property
    def tsize(self):
        """ get thumbnail size """
        width = self.photo.width
        height = self.photo.height
        MAX = 100
        ratio = width / height

        if width > MAX:
            width = MAX
            height = int(width / ratio)
        if height > MAX:
            height = MAX
            width = int(height * ratio)

        return {'w': width, 'h': height}

    @classmethod
    def add_test_comments(cls, peak, count=20):
        """
        add some test comments to the peak
        """
        fake = Faker()

        for __ in range(count):
            man = fake.simple_profile()
            comment = cls(
                peak=peak,
                nickname=man['username'],
                email=man['mail'],
                ip_address=fake.ipv4(),
                body=fake.text(max_nb_chars=80))
            comment.save()
            if random.random() < 0.5:
                reply = cls(
                    peak=peak,
                    parent=comment,
                    nickname=man['username'],
                    email=man['mail'],
                    ip_address=fake.ipv4(),
                    body=fake.text(max_nb_chars=80))
                reply.save()


class Route(models.Model):
    """
    Route model
    """
    peak = models.ForeignKey(
        Peak, on_delete=models.PROTECT, verbose_name=_("peak"))
    name = models.CharField(_("name"), max_length=64, blank=True, null=True)
    slug = models.SlugField(_("slug"), max_length=64, unique=True, null=True)
    number = models.PositiveSmallIntegerField(_("number"), blank=True, null=True)
    short_description = models.TextField(_("short description"), blank=True, null=True)
    description = models.TextField(_("description"), blank=True, null=True)
    recommended_equipment = models.TextField(_("recommended equipment"), blank=True, null=True)
    photo = models.ImageField(
        _("photo"), upload_to=get_image_path, blank=True, null=True)
    map_image = models.ImageField(
        _("map"), upload_to=get_image_path, blank=True, null=True)
    difficulty = models.CharField(_("difficulty"), max_length=3, null=True)
    max_difficulty = models.CharField(_("max difficulty"), max_length=16, null=True)
    length = models.IntegerField(_("length"), blank=True, null=True)
    author = models.CharField(_("author"), max_length=64, blank=True, null=True)
    year = models.IntegerField(_("year"), blank=True, null=True)
    height_difference = models.IntegerField(_("height_difference"), blank=True, null=True)
    start_height = models.IntegerField(_("start_height"), blank=True, null=True)
    descent = models.TextField(_("descent"), blank=True, null=True)
    changed = models.DateTimeField(
        _("created"), default=timezone.now, db_index=True)
    editor = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, verbose_name=_("editor"), null=True)
    ready = models.BooleanField(_("ready"), default=False)

    class Meta:
        db_table = 'route'
        verbose_name = _("route")
        verbose_name_plural = _("routes")

    def __str__(self):
        return f'{self.number}-{self.name}'

    @property
    def sections(self):
        """ route sections """
        return self.routesection_set.order_by('num')

    @property
    def points(self):
        """ route points """
        return self.routepoint_set.order_by('id')

    def photos(self):
        """ route photos """
        return self.routephoto_set.order_by('id')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_name(Route, self.name)
        return super().save(*args, **kwargs)

    def can_be_edited(self, user):
        """
        can the user edit this route
        """
        if user is None:
            return False
        if user.is_anonymous:
            return False
        if user.is_superuser:
            return True
        climber = user.climber
        if climber.is_editor and self.editor == user:
            return True
        return False

    def can_be_removed(self):
        """
        can be removed this route ?
        """
        return True


class RouteSection(models.Model):
    """
    Route Section model
    """
    route = models.ForeignKey(
        Route, on_delete=models.PROTECT, verbose_name=_("route"))
    num = models.IntegerField(_("number"), blank=True, null=True)
    description = models.TextField(_("description"), blank=True, null=True)
    length = models.IntegerField(_("length"), blank=True, null=True)
    angle = models.CharField(_("angle"), max_length=32, blank=True, null=True)
    difficulty = models.CharField(_("difficulty"), max_length=32, blank=True, null=True)

    class Meta:
        db_table = 'route_section'
        verbose_name = _("route section")
        verbose_name_plural = _("route sections")

    def __str__(self):
        return f'{self.id}-{self.num}'

    @property
    def number(self):
        """ get section number """
        return f'R<sub>{self.num - 1}</sub>-R<sub>{self.num}</sub>'

    @property
    def details(self):
        """ get route section details """
        len_km = self.length // 1000 if self.length else None
        len_m = self.length % 1000 if self.length else None
        length = f'{len_m}м' if self.length else ''
        if len_km:
            length = f'{len_km}км ' + length
        items = [length]
        if self.angle:
            items.append(f'{self.angle}&deg;')
        items.append(self.difficulty)

        return ', '.join(items) if all(items) else ''


class RoutePhoto(models.Model):
    """
    Route Photo model
    """
    route = models.ForeignKey(
        Route, on_delete=models.PROTECT, verbose_name=_("route"))
    photo = models.ImageField(
        _("photo"), upload_to=get_image_path, blank=True, null=True)
    description = models.CharField(
        _("description"), max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'route_photo'
        verbose_name = _("route photo")
        verbose_name_plural = _("route photos")

    def __str__(self):
        return f'{self.id}-{self.photo}'

    @property
    def thumbnail(self):
        """ get photo thumbnail """
        return thumbnail(self.photo.width, self.photo.height)


class RoutePoint(models.Model):
    """
    Route Point model
    """
    route = models.ForeignKey(
        Route, on_delete=models.PROTECT, verbose_name=_("route"))
    point = models.ForeignKey(
        GeoPoint, blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name=_("point"))
    description = models.CharField(
        _("description"), max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'route_point'
        verbose_name = _("route point")
        verbose_name_plural = _("route points")

    def __str__(self):
        return f'{self.route.id}-{self.point}'


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    It calculates distance between two points (km).
    https://en.wikipedia.org/wiki/Haversine_formula
    Test: distance between Red Square (55.7539° N, 37.6208° E)
    and Hermitage (59.9398° N, 30.3146° E) equals 634.569km
    """
    earth_radius = 6371.0

    lon1, lat1, lon2, lat2 = map(math.radians, (lon1, lat1, lon2, lat2))

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    aaa = math.sin(dlat / 2) ** 2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon / 2) ** 2

    return earth_radius * 2 * math.asin(math.sqrt(aaa))
