"""
There are Admin Classes to present in admin interface objects
related to common api facilities
"""

from django.contrib import admin
from routes.api.models import App, AppVersion, UserAppVersion


class AppAdmin(admin.ModelAdmin):
    """
    A AppAdmin object encapsulates an instance of the App.
    """
    list_display = (
        'id', 'slug', 'name', 'description', 'added')
    search_fields = ('slug', 'name', 'description')
    ordering = ('slug', )


admin.site.register(App, AppAdmin)


class AppVersionAdmin(admin.ModelAdmin):
    """
    A AppVersionAdmin object encapsulates an instance of the AppVersion.
    """
    list_display = (
        'id', 'app', 'version', 'author', 'created', 'added')
    search_fields = ('version', 'author')
    ordering = ('-created', )


admin.site.register(AppVersion, AppVersionAdmin)


class UserAppVersionAdmin(admin.ModelAdmin):
    """
    A UserAppVersionAdmin object encapsulates an instance of the UserAppVersion
    """
    list_display = (
        'id', 'user', 'app', 'app_version', 'user_app_version',
        'added', 'device', 'os')
    search_fields = ('app_version', 'os', 'device')
    ordering = ('-added', )


admin.site.register(UserAppVersion, UserAppVersionAdmin)
