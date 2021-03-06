"""
Admin classes for models from Carpathians
"""
from django.contrib import admin
from routes.mountains.models import (
    Ridge, GeoPoint, RidgeInfoLink, Peak, PeakPhoto, Route, RouteSection,
    RoutePhoto, RoutePoint)


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
    list_display = ('id', 'slug', 'name', 'description')
    search_fields = ('slug', 'name', 'description')
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
        'height', 'photo', 'point')
    search_fields = ('slug', 'name', 'description')
    raw_id_fields = ('point', )
    list_filter = (RidgeFilter, )
    inlines = [PeakPhotoInline, ]
    ordering = ('name', )


admin.site.register(Peak, PeakAdmin)


class PeakPhotoAdmin(admin.ModelAdmin):
    """ PeakPhotoAdmin """
    list_display = ('id', 'peak', 'photo', 'description')
    search_fields = ('description', )
    ordering = ('-id', )


admin.site.register(PeakPhoto, PeakPhotoAdmin)


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
        'height_difference', 'start_height')
    search_fields = ('name', 'description')
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
