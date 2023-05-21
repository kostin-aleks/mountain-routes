"""
Views for whole project
"""
from datetime import datetime, timedelta

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import translation


def switch_language(request, language):
    """
    switch language of interface
    """
    translation.activate(language)

    response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    max_age = 365 * 24 * 60 * 60  # 10 years
    expires = datetime.now() + timedelta(seconds=max_age)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME,
                        language, expires=expires)
    return response
