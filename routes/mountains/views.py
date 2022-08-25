"""
views related to carpathians
"""

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.utils.html import format_html
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

import django_filters
import django_tables2 as tables
from django_tables2.config import RequestConfig

from routes.mountains.models import (
    Ridge, Peak, Route, GeoPoint, RouteSection, RoutePoint, RoutePhoto,
    PeakPhoto, RidgeInfoLink)
from routes.mountains.forms import (
    RidgeForm, PeakForm, NewPeakForm, RouteForm, RouteSectionForm, RoutePointForm,
    PeakPhotoForm, RidgeLinkForm, RoutePhotoForm, RouteNewPointForm)


def divide_into_groups_of_three(lst):
    """
    divide the list into groups of three
    """
    chunked_list = list()
    chunk_size = 3

    for i in range(0, len(lst), chunk_size):
        chunked_list.append(lst[i:i + chunk_size])

    return chunked_list


class PeakFilter(django_filters.FilterSet):
    """
    Filter Set to filter by peak
    """
    class Meta:
        model = Peak
        fields = []


class PeakTable(tables.Table):
    """
    Table for peaks
    """
    slug = tables.Column(accessor='slug', verbose_name="")
    name = tables.Column(accessor='name', verbose_name="Название")
    height = tables.Column(accessor='height', verbose_name="Высота, м")
    ridge = tables.Column(accessor='ridge__name', verbose_name="Район")

    def render_slug(self, value):
        """render slug"""
        return format_html(
            '<a href="{}">{}</a>',
            reverse('peak', args=[value]),
            value)

    def render_ridge(self, value, record):
        """render field ridge"""
        return format_html(
            '<a href="{}">{}</a>',
            reverse('ridge', args=[record.ridge.slug]),
            value)

    class Meta:
        attrs = {'class': 'table table-striped table-hover'}


class RidgeFilter(django_filters.FilterSet):
    """
    Filter Set to filter by ridge
    """
    class Meta:
        model = Ridge
        fields = []


class RidgeTable(tables.Table):
    """
    Table for ridges
    """
    slug = tables.Column(accessor='slug', verbose_name="")
    name = tables.Column(accessor='name', verbose_name="")

    def render_slug(self, value):
        """render field slug"""
        return format_html(
            '<a href="{}">{}</a>',
            reverse('ridge', args=[value]),
            value)

    class Meta:
        attrs = {'class': 'table table-striped table-hover'}


class RouteFilter(django_filters.FilterSet):
    """
    Filter Set to filter by route
    """
    class Meta:
        model = Route
        fields = []


class RouteTable(tables.Table):
    """
    Table for routes
    """
    route_id = tables.Column(accessor='id', verbose_name="route_id")
    number = tables.Column(accessor='number', verbose_name="#")
    name = tables.Column(accessor='name', verbose_name="Название")
    difficulty = tables.Column(accessor='difficulty', verbose_name="КТ")
    peak = tables.Column(accessor='peak__name', verbose_name="Вершина")
    height = tables.Column(accessor='peak__height', verbose_name="Высота")
    author = tables.Column(accessor='author', verbose_name="Автор")
    year = tables.Column(accessor='year', verbose_name="Год")

    def render_route_id(self, value):
        """render field route_id"""
        return format_html(
            '<a href="{}">{}</a>',
            reverse('route', args=[value]),
            value)

    def render_peak(self, value, record):
        """render field peak"""
        return format_html(
            '<a href="{}">{}</a>',
            reverse('peak', args=[record.peak.slug]),
            value)

    def render_name(self, value, record):
        """render field name"""
        return format_html(
            '<a href="{}">{}</a>',
            reverse('route', args=[record.id]),
            value)

    class Meta:
        attrs = {'class': 'table table-striped table-hover'}


def ridges(request):
    """
    return page with ridges
    """
    user = request.user

    order_by = 'name'
    qs = Ridge.objects.all().order_by(order_by)

    _filter = RidgeFilter(request.GET, queryset=qs)

    ridge_table = RidgeTable(_filter.qs)
    RequestConfig(
        request, paginate={"per_page": 100}).configure(ridge_table)

    return render(
        request,
        'Routes/ridges.html',
        {
            'table': ridge_table,
            'can_edit': user.is_superuser or (user.is_authenticated and user.climber.is_editor),
        })


def ridge(request, slug):
    """
    return page with ridge
    """
    the_ridge = get_object_or_404(Ridge, slug=slug)

    return render(
        request,
        'Routes/ridge.html',
        {
            'ridge': the_ridge,
            'can_be_edited': the_ridge.can_be_edited(request.user),
            'can_be_removed': the_ridge.can_be_removed()})


def peak(request, slug):
    """
    return page for the peak
    """
    the_peak = get_object_or_404(Peak, slug=slug)

    return render(
        request,
        'Routes/peak.html',
        {
            'peak': the_peak,
            'photos': divide_into_groups_of_three(the_peak.photos()),
            'can_be_edited': the_peak.can_be_edited(request.user),
            'can_be_removed': the_peak.can_be_removed()})


def route(request, route_id):
    """
    return page for the route
    """
    the_route = get_object_or_404(Route, pk=route_id)

    return render(
        request,
        'Routes/route.html',
        {
            'route': the_route,
            'photos': divide_into_groups_of_three(the_route.photos()),
            'can_be_edited': the_route.can_be_edited(request.user),
            'can_be_removed': the_route.can_be_removed()
        })


def routes(request):
    """
    return list of routes
    """
    order_by = 'number'
    qs = Route.objects.all().order_by(order_by)

    _filter = RouteFilter(request.GET, queryset=qs)

    routes_table = RouteTable(_filter.qs)
    RequestConfig(
        request, paginate={"per_page": 100}).configure(routes_table)

    return render(
        request,
        'Routes/routes.html',
        {'table': routes_table})


def peaks(request):
    """
    return list of peaks
    """
    order_by = 'name'
    qs = Peak.objects.all().order_by(order_by)

    _filter = PeakFilter(request.GET, queryset=qs)

    peaks_table = PeakTable(_filter.qs)
    RequestConfig(
        request, paginate={"per_page": 100}).configure(peaks_table)

    return render(
        request,
        'Routes/peaks.html',
        {'table': peaks_table})


@login_required
def add_ridge(request):
    """
    add a new ridge
    """
    user = request.user
    if not (user.is_superuser or user.climber.is_editor):
        raise PermissionDenied()

    if request.method == 'POST':
        form = RidgeForm(request.POST)
        if 'add' in request.POST and form.is_valid():
            data = form.cleaned_data
            Ridge.objects.create(
                slug=data['slug'],
                name=data['name'],
                description=data['description'])
            return HttpResponseRedirect(reverse('ridges'))
    else:
        form = RidgeForm()

    args = {}
    args['form'] = form

    return render(
        request,
        'Routes/add_ridge.html',
        args)


@login_required
def remove_ridge(request, slug):
    """
    remove the ridge
    """
    user = request.user
    the_ridge = get_object_or_404(Ridge, slug=slug)
    if not (user.is_superuser or (user.climber.is_editor and the_ridge.editor == user)):
        raise PermissionDenied()

    if request.method == 'POST':
        data = request.POST
        if 'remove' in data:
            Ridge.objects.filter(slug=data['slug']).delete()
            return HttpResponseRedirect(reverse('ridges'))
        if 'cancel' in data:
            return HttpResponseRedirect(reverse('ridge', args=[the_ridge.slug]))

    args = {'ridge': the_ridge}

    return render(
        request,
        'Routes/remove_ridge.html',
        args)


@login_required
def add_ridge_peak(request, slug):
    """
    edit the ridge
    """
    user = request.user
    the_ridge = get_object_or_404(Ridge, slug=slug)
    if not (user.is_superuser or (user.climber.is_editor and the_ridge.editor == user)):
        raise PermissionDenied()

    if request.method == 'POST':
        form = NewPeakForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            latitude = GeoPoint.coordinate_from_string(data['latitude'])
            longitude = GeoPoint.coordinate_from_string(data['longitude'])

            Peak.objects.create(
                ridge=the_ridge,
                slug=data['slug'],
                name=data['name'],
                description=data['description'],
                height=data['height'],
                photo=request.FILES.get('photo'),
                point=GeoPoint.objects.create(latitude=latitude, longitude=longitude)
            )
            return HttpResponseRedirect(reverse('ridge', args=[the_ridge.slug]))
    else:
        form = NewPeakForm()

    args = {
        'form': form,
        'ridge': the_ridge
    }

    return render(
        request,
        'Routes/add_ridge_peak.html',
        args)


@login_required
def edit_ridge(request, slug):
    """
    edit the ridge
    """
    user = request.user
    the_ridge = get_object_or_404(Ridge, slug=slug)
    if not (user.is_superuser or \
            (user.climber.is_editor and the_ridge.editor == user)):
        raise PermissionDenied()

    if request.method == 'POST':
        form = RidgeForm(request.POST, instance=the_ridge)

        if form.is_valid():
            data = form.cleaned_data
            the_ridge.slug = data['slug']
            the_ridge.name = data['name']
            the_ridge.description = data['description']
            the_ridge.save()

            return HttpResponseRedirect(reverse('ridges'))
    else:
        form = RidgeForm(instance=the_ridge)

    args = {}
    args['form'] = form
    args['form_link'] = RidgeLinkForm()
    args['ridge'] = the_ridge

    return render(
        request, 'Routes/edit_ridge.html', args)


@login_required
def edit_peak(request, slug):
    """
    edit the peak
    """
    user = request.user
    the_peak = get_object_or_404(Peak, slug=slug)
    if not (user.is_superuser or
            (user.climber.is_editor and the_peak.editor == user)):
        raise PermissionDenied()

    if request.method == 'POST':
        form = PeakForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            latitude = abs(data['latitude_degree']) + data['latitude_minute'] / 60.0 \
                + data['latitude_second'] / 3600.0
            if data['latitude_degree'] < 0:
                latitude = - latitude
            longitude = abs(data['longitude_degree']) + data['longitude_minute'] / \
                60.0 + data['longitude_second'] / 3600.0
            if data['longitude_degree'] < 0:
                longitude = - longitude

            the_peak.slug = data['slug']
            the_peak.name = data['name']
            the_peak.description = data['description']
            the_peak.height = data['height']
            if request.FILES.get('photo'):
                the_peak.photo = request.FILES.get('photo')
            the_peak.point.latitude = latitude
            the_peak.point.longitude = longitude
            the_peak.point.save()
            the_peak.save()

            return HttpResponseRedirect(reverse('peak', args=[the_peak.slug]))
    else:
        data = {
            'slug': the_peak.slug,
            'name': the_peak.name,
            'description': the_peak.description,
            'height': the_peak.height,
            'photo': the_peak.photo
        }
        fill_with_point_data(the_peak.point, data)

        form = PeakForm(initial=data)

    form_photo = PeakPhotoForm()

    args = {}
    args['form'] = form
    args['peak'] = the_peak
    args['form_photo'] = form_photo

    return render(
        request, 'Routes/edit_peak.html', args)


@login_required
def remove_peak(request, slug):
    """
    remove the peak
    """
    user = request.user
    the_peak = get_object_or_404(Peak, slug=slug)
    the_ridge = the_peak.ridge
    if not (user.is_superuser or
            (user.climber.is_editor and the_peak.editor == user)):
        raise PermissionDenied()

    if request.method == 'POST':
        data = request.POST
        if 'remove' in data:
            Peak.objects.filter(slug=data['slug']).delete()
            return HttpResponseRedirect(reverse('ridge', args=[the_ridge.slug]))
        if 'cancel' in data:
            return HttpResponseRedirect(reverse('peak', args=[the_peak.slug]))

    args = {'peak': the_peak}

    return render(
        request,
        'Routes/remove_peak.html',
        args)


@login_required
def add_peak_route(request, slug):
    """
    add a new route to the peak
    """
    user = request.user
    the_peak = get_object_or_404(Peak, slug=slug)
    if not (user.is_superuser or \
            (user.climber.is_editor and the_peak.editor == user)):
        raise PermissionDenied()

    if request.method == 'POST':
        form = RouteForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            Route.objects.create(
                peak=the_peak,
                slug=data['slug'],
                name=data['name'],
                description=data['description'],
                short_description=data['short_description'],
                length=data['length'],
                difficulty=data['difficulty'],
                max_difficulty=data['max_difficulty'],
                author=data['author'],
                year=data['year'],
                height_difference=data['height_difference'],
                start_height=data['start_height'],
                descent=data['descent'],
                editor=user,
                ready=data['ready'],
            )
            return HttpResponseRedirect(reverse('peak', args=[the_peak.slug]))
    else:
        form = RouteForm()

    args = {
        'form': form,
        'peak': the_peak,
    }

    return render(
        request, 'Routes/add_peak_route.html', args)


@login_required
def edit_route(request, route_id):
    """
    edit the route
    """
    user = request.user
    the_route = get_object_or_404(Route, id=route_id)
    if not (user.is_superuser or \
            (user.climber.is_editor and the_route.editor == user)):
        raise PermissionDenied()

    if request.method == 'POST':
        form = RouteForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            the_route.slug = data['slug']
            the_route.name = data['name']
            the_route.description = data['description']
            the_route.short_description = data['short_description']
            the_route.recommended_equipment = data['recommended_equipment']
            the_route.length = data['length']
            the_route.difficulty = data['difficulty']
            the_route.max_difficulty = data['max_difficulty']
            the_route.author = data['author']
            the_route.year = data['year']
            the_route.height_difference = data['height_difference']
            the_route.start_height = data['start_height']
            the_route.descent = data['descent']
            the_route.ready = data['ready']
            if request.FILES.get('photo'):
                the_route.photo = request.FILES.get('photo')
            if request.FILES.get('map_image'):
                the_route.map_image = request.FILES.get('map_image')
            the_route.save()

            return HttpResponseRedirect(reverse('route', args=[the_route.id]))
    else:
        data = {
            'slug': the_route.slug,
            'name': the_route.name,
            'description': the_route.description,
            'short_description': the_route.short_description,
            'recommended_equipment': the_route.recommended_equipment,
            'length': the_route.length,
            'difficulty': the_route.difficulty,
            'max_difficulty': the_route.max_difficulty,
            'author': the_route.author,
            'year': the_route.year,
            'height_difference': the_route.height_difference,
            'start_height': the_route.start_height,
            'descent': the_route.descent,
            'ready': the_route.ready,
            'photo': the_route.photo,
            'map_image': the_route.map_image,
        }
        form = RouteForm(initial=data)

    form_section = RouteSectionForm()
    form_point = RouteNewPointForm()
    form_photo = RoutePhotoForm()

    args = {}
    args['form'] = form
    args['route'] = the_route
    args['form_section'] = form_section
    args['form_point'] = form_point
    args['form_photo'] = form_photo

    return render(
        request, 'Routes/edit_route.html', args)


@login_required
def remove_route(request, route_id):
    """
    remove the route
    """
    user = request.user
    the_route = get_object_or_404(Route, id=route_id)
    the_peak = the_route.peak
    if not (user.is_superuser or \
            (user.climber.is_editor and the_route.editor == user)):
        raise PermissionDenied()

    if request.method == 'POST':
        data = request.POST
        if 'remove' in data:
            for _route in Route.objects.filter(slug=data['slug']):
                RouteSection.objects.filter(route=_route).delete()
                RoutePoint.objects.filter(route=_route).delete()
            Route.objects.filter(slug=data['slug']).delete()
            return HttpResponseRedirect(reverse('peak', args=[the_peak.slug]))
        if 'cancel' in data:
            return HttpResponseRedirect(reverse('route', args=[the_route.id]))

    args = {'route': the_route}

    return render(
        request,
        'Routes/remove_route.html',
        args)


@login_required
def add_route_section(request, route_id):
    """
    add a new route section
    """
    user = request.user
    the_route = get_object_or_404(Route, id=route_id)
    if not (user.is_superuser or \
            (user.climber.is_editor and the_route.editor == user)):
        raise PermissionDenied()

    if request.method == 'POST':
        form = RouteSectionForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            RouteSection.objects.create(
                route=the_route,
                num=data['num'],
                description=data['description'],
                length=data['length'],
                difficulty=data['difficulty'],
                angle=data['angle']
            )

    args = {}
    args['form'] = form
    args['route'] = the_route
    args['sections'] = the_route.sections

    return render(
        request, 'Routes/route_sections.html', args)


@login_required
def add_peak_photo(request, slug):
    """
    add a new peak photo
    """
    user = request.user
    the_peak = get_object_or_404(Peak, slug=slug)
    if not (user.is_superuser or (user.climber.is_editor and the_peak.editor == user)):
        raise PermissionDenied()

    if request.method == 'POST':
        form = PeakPhotoForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            peak_photo = PeakPhoto.objects.create(
                peak=the_peak,
                description=data['description'],
            )
            if request.FILES.get('photo'):
                peak_photo.photo = request.FILES.get('photo')
                peak_photo.save()

    args = {}
    args['peak'] = the_peak

    return render(
        request, 'Routes/peak_photos.html', args)


@login_required
def add_route_photo(request, route_id):
    """
    add a new route photo
    """
    user = request.user
    the_route = get_object_or_404(Route, id=route_id)
    if not (user.is_superuser or \
            (user.climber.is_editor and the_route.editor == user)):
        raise PermissionDenied()

    if request.method == 'POST':
        form = RoutePhotoForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            route_photo = RoutePhoto.objects.create(
                route=the_route,
                description=data['description'],
            )
            if request.FILES.get('photo'):
                route_photo.photo = request.FILES.get('photo')
                route_photo.save()

    args = {}
    args['route'] = the_route

    return render(
        request, 'Routes/route_photos.html', args)


@login_required
def add_route_point(request, route_id):
    """
    add a new route point
    """
    user = request.user
    the_route = get_object_or_404(Route, id=route_id)
    if not (user.is_superuser or \
            (user.climber.is_editor and the_route.editor == user)):
        raise PermissionDenied()

    if request.method == 'POST':
        form = RouteNewPointForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            latitude = GeoPoint.coordinate_from_string(data['latitude'])
            longitude = GeoPoint.coordinate_from_string(data['longitude'])
            _point = GeoPoint.objects.create(
                latitude=latitude,
                longitude=longitude,
            )
            RoutePoint.objects.create(
                point=_point,
                description=data['description'],
                route=the_route)

    args = {}
    args['route'] = the_route

    return render(
        request, 'Routes/route_points.html', args)


@login_required
def add_ridge_link(request, slug):
    """
    add a new ridge link
    """
    user = request.user
    the_ridge = get_object_or_404(Ridge, slug=slug)
    if not (user.is_superuser or \
            (user.climber.is_editor and the_ridge.editor == user)):
        raise PermissionDenied()

    if request.method == 'POST':
        form = RidgeLinkForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            RidgeInfoLink.objects.create(
                link=data['link'],
                description=data['description'],
                ridge=the_ridge)
    else:
        form = RidgeLinkForm()
    args = {}
    args['ridge'] = the_ridge

    return render(
        request, 'Routes/ridge_links.html', args)


@login_required
@csrf_exempt
def remove_route_point(request, route_id, point_id):
    """
    remove a new route point
    """
    user = request.user
    the_route = get_object_or_404(Route, id=route_id)
    if not (user.is_superuser or \
            (user.climber.is_editor and the_route.editor == user)):
        raise PermissionDenied()
    the_point = get_object_or_404(RoutePoint, id=point_id)
    if the_point.route.id != the_route.id:
        raise Http404

    the_point.delete()

    return render(
        request, 'Routes/delete_route_point.html', {})


@login_required
@csrf_exempt
def remove_route_photo(request, route_id, photo_id):
    """
    remove a new route photo
    """
    user = request.user
    the_route = get_object_or_404(Route, id=route_id)
    if not (user.is_superuser or \
            (user.climber.is_editor and the_route.editor == user)):
        raise PermissionDenied()
    the_photo = get_object_or_404(RoutePhoto, id=photo_id)
    if the_photo.route.id != the_route.id:
        raise Http404

    the_photo.delete()

    return render(
        request, 'Routes/delete_route_photo.html', {})


@login_required
@csrf_exempt
def remove_ridge_link(request, slug, link_id):
    """
    remove a new ridge link
    """
    user = request.user
    the_ridge = get_object_or_404(Ridge, slug=slug)
    if not (user.is_superuser or \
            (user.climber.is_editor and the_ridge.editor == user)):
        raise PermissionDenied()
    the_link = get_object_or_404(RidgeInfoLink, id=link_id)
    if the_link.ridge.id != the_ridge.id:
        raise Http404

    the_link.delete()

    return render(
        request, 'Routes/delete_ridge_link.html', {})


@login_required
@csrf_exempt
def remove_route_section(request, route_id, section_id):
    """
    remove a new route section
    """
    user = request.user
    the_route = get_object_or_404(Route, id=route_id)
    if not (user.is_superuser or \
            (user.climber.is_editor and the_route.editor == user)):
        raise PermissionDenied()
    the_section = get_object_or_404(RouteSection, id=section_id)
    if the_section.route.id != the_route.id:
        raise Http404

    the_section.delete()

    return render(
        request, 'Routes/delete_route_section.html', {})


@login_required
@csrf_exempt
def remove_peak_photo(request, slug, photo_id):
    """
    remove a new peak photo
    """
    user = request.user
    the_peak = get_object_or_404(Peak, slug=slug)
    if not (user.is_superuser or \
            (user.climber.is_editor and the_peak.editor == user)):
        raise PermissionDenied()
    the_photo = get_object_or_404(PeakPhoto, id=photo_id)
    if the_photo.peak.id != the_peak.id:
        raise Http404

    the_photo.delete()

    return render(
        request, 'Routes/delete_peak_photo.html', {})


def fill_with_point_data(point, data):
    """
    fill form fields with point data
    """
    data['latitude_degree'] = point.degrees('lat')
    data['latitude_minute'] = point.minutes('lat')
    data['latitude_second'] = point.seconds('lat')
    data['longitude_degree'] = point.degrees('lon')
    data['longitude_minute'] = point.minutes('lon')
    data['longitude_second'] = point.seconds('lon')


@login_required
def edit_route_point(request, route_id, point_id):
    """
    edit a new route point
    """
    user = request.user
    the_route = get_object_or_404(Route, id=route_id)
    if not (user.is_superuser or \
            (user.climber.is_editor and the_route.editor == user)):
        raise PermissionDenied()
    the_point = get_object_or_404(RoutePoint, id=point_id)
    if the_point.route.id != the_route.id:
        raise Http404

    data = {'description': the_point.description}
    fill_with_point_data(the_point.point, data)

    form = RoutePointForm(initial=data)

    return render(
        request,
        'Routes/edit_route_point.html',
        {'route': the_route, 'point': the_point, 'form_point': form})


@login_required
def edit_ridge_link(request, slug, link_id):
    """
    edit a new ridge link
    """
    user = request.user
    the_ridge = get_object_or_404(Ridge, slug=slug)
    if not (user.is_superuser or \
            (user.climber.is_editor and the_ridge.editor == user)):
        raise PermissionDenied()
    the_link = get_object_or_404(RidgeInfoLink, id=link_id)
    if the_link.ridge.id != the_ridge.id:
        raise Http404

    data = {
        'description': the_link.description,
        'link': the_link.link,
    }

    form = RidgeLinkForm(initial=data)

    return render(
        request,
        'Routes/edit_ridge_link.html',
        {'ridge': the_ridge, 'link': the_link, 'form_link': form})


@login_required
def edit_route_section(request, route_id, section_id):
    """
    edit a new route section
    """
    user = request.user
    the_route = get_object_or_404(Route, id=route_id)
    if not (user.is_superuser or \
            (user.climber.is_editor and the_route.editor == user)):
        raise PermissionDenied()
    the_section = get_object_or_404(RouteSection, id=section_id)
    if the_section.route.id != the_route.id:
        raise Http404

    data = {
        'description': the_section.description,
        'num': the_section.num,
        'length': the_section.length,
        'angle': the_section.angle,
        'difficulty': the_section.difficulty,
    }

    form = RouteSectionForm(initial=data)

    return render(
        request,
        'Routes/edit_route_section.html',
        {'route': the_route, 'section': the_section, 'form_section': form})


@login_required
def get_route_point(request, route_id, point_id):
    """
    get the route point
    """
    user = request.user
    the_route = get_object_or_404(Route, id=route_id)
    if not (user.is_superuser or \
            (user.climber.is_editor and the_route.editor == user)):
        raise PermissionDenied()
    the_point = get_object_or_404(RoutePoint, id=point_id)
    if the_point.route.id != the_route.id:
        raise Http404

    return render(
        request,
        'Routes/get_route_point.html',
        {'route': the_route, 'point': the_point})


@login_required
def get_ridge_link(request, slug, link_id):
    """
    get the ridge link
    """
    user = request.user
    the_ridge = get_object_or_404(Ridge, slug=slug)
    if not (user.is_superuser or \
            (user.climber.is_editor and the_ridge.editor == user)):
        raise PermissionDenied()
    the_link = get_object_or_404(RidgeInfoLink, id=link_id)
    if the_link.ridge.id != the_ridge.id:
        raise Http404

    return render(
        request,
        'Routes/get_ridge_link.html',
        {'ridge': the_ridge, 'link': the_link})


@login_required
def get_route_section(request, route_id, section_id):
    """
    get the route section
    """
    user = request.user
    the_route = get_object_or_404(Route, id=route_id)
    if not (user.is_superuser or \
            (user.climber.is_editor and the_route.editor == user)):
        raise PermissionDenied()
    the_section = get_object_or_404(RouteSection, id=section_id)
    if the_section.route.id != the_route.id:
        raise Http404

    return render(
        request,
        'Routes/get_route_section.html',
        {'route': the_route, 'section': the_section})


@login_required
@csrf_exempt
def update_route_point(request, route_id, point_id):
    """
    update a new route point
    """
    user = request.user
    the_route = get_object_or_404(Route, id=route_id)
    if not (user.is_superuser or \
            (user.climber.is_editor and the_route.editor == user)):
        raise PermissionDenied()
    the_point = get_object_or_404(RoutePoint, id=point_id)
    if the_point.route.id != the_route.id:
        raise Http404

    if request.method == 'POST':
        form = RoutePointForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            latitude = abs(data['latitude_degree']) + data['latitude_minute'] / 60.0 \
                + data['latitude_second'] / 3600.0
            if data['latitude_degree'] < 0:
                latitude = - latitude
            longitude = abs(data['longitude_degree']) + data['longitude_minute'] / \
                60.0 + data['longitude_second'] / 3600.0
            if data['longitude_degree'] < 0:
                longitude = - longitude
            the_point.point.latitude = latitude
            the_point.point.longitude = longitude

            the_point.description = data['description']
            the_point.save()
            return render(
                request, 'Routes/get_route_point.html',
                {'route': the_route, 'point': the_point})

        return render(
            request, 'Routes/edit_route_point.html',
            {'route': the_route, 'point': the_point, 'form': form})

    args = {}
    args['route'] = the_route
    args['point'] = the_point

    return render(
        request, 'Routes/get_route_point.html', args)


@login_required
@csrf_exempt
def update_ridge_link(request, slug, link_id):
    """
    update a new ridge link
    """
    user = request.user
    the_ridge = get_object_or_404(Ridge, slug=slug)
    if not (user.is_superuser or \
            (user.climber.is_editor and the_ridge.editor == user)):
        raise PermissionDenied()
    the_link = get_object_or_404(RidgeInfoLink, id=link_id)
    if the_link.ridge.id != the_ridge.id:
        raise Http404

    if request.method == 'POST':
        form = RidgeLinkForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            the_link.description = data['description']
            the_link.link = data['link']
            the_link.save()
            return render(
                request, 'Routes/get_ridge_link.html',
                {'ridge': the_ridge, 'link': the_link})

        return render(
            request, 'Routes/edit_ridge_link.html',
            {'ridge': the_ridge, 'link': the_link, 'form': form})

    args = {}
    args['ridge'] = the_ridge
    args['link'] = the_link

    return render(
        request, 'Routes/get_ridge_link.html', args)


@login_required
@csrf_exempt
def update_route_section(request, route_id, section_id):
    """
    update a new route section
    """
    user = request.user
    the_route = get_object_or_404(Route, id=route_id)
    if not (user.is_superuser or \
            (user.climber.is_editor and the_route.editor == user)):
        raise PermissionDenied()
    the_section = get_object_or_404(RouteSection, id=section_id)
    if the_section.route.id != the_route.id:
        raise Http404

    if request.method == 'POST':
        form = RouteSectionForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            the_section.num = data['num']
            the_section.length = data['length']
            the_section.angle = data['angle']
            the_section.description = data['description']
            the_section.save()
            return render(
                request, 'Routes/get_route_section.html',
                {'route': the_route, 'section': the_section})

        return render(
            request, 'Routes/edit_route_section.html',
            {'route': the_route, 'section': the_section, 'form': form})

    args = {}
    args['route'] = the_route
    args['point'] = the_section

    return render(
        request, 'Routes/get_route_section.html', args)
