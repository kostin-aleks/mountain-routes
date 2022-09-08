"""
Context variables
"""
from django.conf import settings


def global_context(request):
    """
    All global context variables we might need for project template rendering
    """
    language_switch = {}
    if len(settings.LANGUAGE_CODES) > 1:
        language_switch = {k: settings.DEFINED_LANGUAGES[k]['short'] for k in settings.LANGUAGE_CODES}
    return {
        'LANGUAGE_SWITCH': language_switch,
    }
