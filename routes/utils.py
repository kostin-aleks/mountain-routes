"""
Module stores utilities
"""
import os
import random
from datetime import datetime
import string
import requests

from django.conf import settings
from django.shortcuts import _get_queryset
from django.utils.translation import gettext_lazy as _


ANY = 'any'
TEST_LOGIN = ''
TEST_PASSWD = 'newstrongpassword'


def class_name(instance):
    """
    returns name of class for the object
    """
    return instance.__class__.__name__.lower()


def get_image_path(instance, filename):
    """
    returns path related to type of object and current datetime
    """
    now = datetime.now()
    return os.path.join(
        'photos',
        class_name(instance),
        now.strftime('%Y%m%d%H%M'), filename)


def get_object_or_none(klass, *args, **kwargs):
    """
    returns object by args or None
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def media_url(request, url):
    """
    creates media url for the local url
    """
    if request and url:
        return request.build_absolute_uri(url)
    return url


def image_url(image):
    """
    checks image and returns image local url
    """
    if image is not None:
        try:
            url = image.url
        except ValueError:
            url = ''
        return url
    return ''


def random_username():
    """
    returns random username compozed with adjective and noun
    """
    MAXLEN = 6
    DIGIT_COUNT = 3

    with open(
            os.path.join(settings.STATICFILES_DIRS[0], 'animals.txt'),
            encoding="utf-8") as _file:
        nouns = _file.readlines()
    nouns = [s for s in nouns if len(s) <= MAXLEN]

    with open(
            os.path.join(settings.STATICFILES_DIRS[0], 'adjectives.txt'),
            encoding="utf-8") as _file:
        adjs = _file.readlines()
    adjs = [s for s in adjs if len(s) <= MAXLEN]

    noun = random.choice(nouns)
    adj = 'longestadjective'
    while len(noun) + len(adj) > MAXLEN * 2 - 1:
        adj = random.choice(adjs)
    adj = adj.strip()
    noun = noun.strip()
    digits = ''.join(random.choices(string.digits, k=DIGIT_COUNT))

    return f'{adj}_{noun}_{digits}'


def ridges_list():
    """
    actual list of ridges
    """
    from routes.mountains.models import Ridge
    first = [('', _('--any--'))]
    return first + [(c.slug, c.name) for c
                    in Ridge.objects.all().order_by('name')]


def peaks_list():
    """
    actual list of peaks
    """
    from routes.mountains.models import Peak
    first = [('', _('--any--'))]
    return first + [(c.slug, c.name) for c
                    in Peak.objects.all().order_by('name')]


def get_ip():
    """
    get IP address from response
    """
    response = requests.get('https://api64.ipify.org?format=json', timeout=20).json()
    return response["ip"]


def ip_geolocation(ip_address='127.0.0.1'):
    """
    Get geolocation by IP location
    """
    if ip_address == '127.0.0.1':
        ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/', timeout=20).json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name"),
        "country_code": response.get("country_code"),
    }
    return location_data
