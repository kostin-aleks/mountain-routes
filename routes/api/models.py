"""
This module stores ORM models related to API
"""
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import JSONField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class App(models.Model):
    """
    Application
    """
    slug = models.SlugField(_("slug"), unique=True)
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"))
    added = models.DateTimeField(_("added"), default=timezone.now)

    def __str__(self):
        return self.slug

    class Meta:
        db_table = 'app'
        verbose_name = _("application")
        verbose_name_plural = _("applications")


class AppVersion(models.Model):
    """
    Application version
    """
    app = models.ForeignKey(
        App, on_delete=models.PROTECT, verbose_name=_("application"),
        related_name='applicationversion')
    version = models.CharField(_("version"), max_length=255)
    author = models.CharField(_("author"), max_length=128)
    created = models.DateTimeField(_("created"))
    added = models.DateTimeField(_("added"), default=timezone.now)

    def __str__(self):
        return self.version

    class Meta:
        db_table = 'app_version'
        verbose_name = _("application version")
        verbose_name_plural = _("application versions")

    @classmethod
    def newest_version(cls, app_slug):
        """
        newest version of application by slug
        """
        return cls.objects.filter(
            app__slug=app_slug).order_by('-added').first()


class UserAppVersion(models.Model):
    """
    User application version
    """
    user = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, verbose_name=_("user"),
        related_name='appveruser')
    app = models.ForeignKey(
        App, on_delete=models.PROTECT, verbose_name=_("application"),
        related_name='userapp')
    app_version = models.CharField(
        _("version"), max_length=255, null=True, blank=True)
    user_app_version = models.CharField(
        _("user-version"), max_length=255, null=True, blank=True)
    device = models.CharField(
        _("device"), null=True, blank=True, max_length=255)
    os = models.CharField(_("OS"), null=True, blank=True, max_length=64)  # pylint: disable=invalid-name
    added = models.DateTimeField(_("added"), default=timezone.now)

    def __str__(self):
        return f'{self.user.username}-{self.app.slug}-{self.app_version}'

    class Meta:
        db_table = 'user_app_version'
        verbose_name = _("user application version")
        verbose_name_plural = _("user application versions")
