"""
There are Admin Classes to present in admin interface objects related to User
"""
from django.contrib import admin
from routes.user.models import Climber, EditorRole


class ClimberAdmin(admin.ModelAdmin):
    """ Climber Admin """
    list_display = (
        'user', 'middle_name', 'geocity')


admin.site.register(Climber, ClimberAdmin)


class EditorRoleAdmin(admin.ModelAdmin):
    """ Editor Role Admin """
    list_display = ('climber',)

admin.site.register(EditorRole, EditorRoleAdmin)
