"""
models for user
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _

from routes.signals import create_custom_user
from routes.geoname.models import GeoCity


User = get_user_model()
signals.post_save.connect(create_custom_user, sender=User)


class Climber(models.Model):
    """ Climber """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_('user'))
    geocity = models.ForeignKey(
        GeoCity, null=True, db_index=True, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = 'climber'

    def __str__(self):
        return f'user {self.user.username}: '

    def address(self):
        """ user address """
        return self.geocity.address_string() if self.geocity else ''

    def get_profile(self):
        """ get user profile """
        return self

    @property
    def is_banned(self):
        """ is user banned ? """
        return False
