"""
Admin classes for models from mountains
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from routes.mountains.models import (
    Ridge, GeoPoint, RidgeInfoLink, Peak, PeakPhoto, PeakComment,
    Route, RouteSection, RoutePhoto, RoutePoint)


class RidgeFilter(admin.SimpleListFilter):
    """ RidgeFilter """
    title = 'Ridge'
    parameter_name = 'ridge'

    def lookups(self, request, model_admin):
        return Ridge.objects.values_list('id', 'name').order_by('name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.distinct().filter(ridge__id=self.value())
        return queryset


class RidgeAdmin(admin.ModelAdmin):
    """ RidgeAdmin """
    list_display = ('id', 'slug', 'name', 'description', 'editor', 'changed', )
    search_fields = ('slug', 'name', 'description')
    raw_id_fields = ('editor',)
    ordering = ('name',)


admin.site.register(Ridge, RidgeAdmin)


class GeoPointAdmin(admin.ModelAdmin):
    """ GeoPointAdmin """
    list_display = ('id', 'latitude', 'longitude')


admin.site.register(GeoPoint, GeoPointAdmin)


class RidgeInfoLinkAdmin(admin.ModelAdmin):
    """ RidgeInfoLinkAdmin """
    list_display = ('id', 'ridge', 'link', 'description')


admin.site.register(RidgeInfoLink, RidgeInfoLinkAdmin)


class PeakPhotoInline(admin.TabularInline):
    """ PeakPhotoInline """
    model = PeakPhoto


class PeakAdmin(admin.ModelAdmin):
    """ PeakAdmin """
    list_display = (
        'id', 'slug', 'name', 'description', 'ridge',
        'height', 'photo', 'point', 'editor', 'changed')
    search_fields = ('slug', 'name', 'description')
    raw_id_fields = ('point', 'editor')
    list_filter = (RidgeFilter, )
    inlines = [PeakPhotoInline, ]
    ordering = ('name', )


admin.site.register(Peak, PeakAdmin)


class PeakFilter(admin.SimpleListFilter):
    """ PeakFilter """
    title = _('Peak')
    parameter_name = 'peak'

    def lookups(self, request, model_admin):
        return Peak.objects.values_list('id', 'name').order_by('name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.distinct().filter(peak__id=self.value())
        return queryset


class PeakPhotoAdmin(admin.ModelAdmin):
    """ PeakPhotoAdmin """
    list_display = ('id', 'peak', 'photo', 'description')
    search_fields = ('description', )
    ordering = ('-id', )


admin.site.register(PeakPhoto, PeakPhotoAdmin)


class PeakCommentAdmin(admin.ModelAdmin):
    """ PeakCommentAdmin """
    list_display = ('id', 'peak', 'body', 'author', 'nickname',
                    'email', 'homepage', 'parent', 'photo', 'doc',
                    'ip_address', 'country_code', 'country', 'region', 'city',
                    'created_on', 'active')
    search_fields = ('body', )
    ordering = ('-id', )
    list_filter = (PeakFilter, )
    raw_id_fields = ('parent',)
    actions = ['hide_comments', 'show_comments']

    def hide_comments(self, request, queryset):
        """ action to hide selected comments """
        queryset.update(active=False)

    def show_comments(self, request, queryset):
        """ action to show selected comments """
        queryset.update(active=True)


admin.site.register(PeakComment, PeakCommentAdmin)


class SectionInline(admin.TabularInline):
    """ SectionInline """
    model = RouteSection


class RoutePointInline(admin.TabularInline):
    """ RoutePointInline """
    model = RoutePoint


class RoutePhotoInline(admin.TabularInline):
    """ RoutePhotoInline """
    model = RoutePhoto


class RouteAdmin(admin.ModelAdmin):
    """ RouteAdmin """
    list_display = (
        'id', 'peak', 'name', 'number',
        'description', 'photo', 'map_image', 'descent',
        'difficulty', 'max_difficulty', 'length',
        'author', 'year',
        'height_difference', 'start_height',
        'editor', 'changed',
    )
    search_fields = ('name', 'description')
    raw_id_fields = ('editor', )
    inlines = [SectionInline, RoutePointInline, RoutePhotoInline]
    ordering = ('peak__name', 'name')


admin.site.register(Route, RouteAdmin)


class RouteSectionAdmin(admin.ModelAdmin):
    """ RouteSectionAdmin """
    list_display = ('id', 'route', 'num', 'description', 'difficulty',
                    'length', 'angle')
    ordering = ('route__name', 'num')


admin.site.register(RouteSection, RouteSectionAdmin)


class RoutePhotoAdmin(admin.ModelAdmin):
    """ RoutePhotoAdmin """
    list_display = ('id', 'route', 'photo', 'description')
    ordering = ('route__name', '-id')


admin.site.register(RoutePhoto, RoutePhotoAdmin)


class RoutePointAdmin(admin.ModelAdmin):
    """ RoutePointAdmin """
    list_display = ('id', 'route', 'point', 'description')
    raw_id_fields = ('point', )
    ordering = ('route__name', '-id')


admin.site.register(RoutePoint, RoutePointAdmin)
