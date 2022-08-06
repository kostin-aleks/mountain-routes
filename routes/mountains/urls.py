"""
urls for mountains
"""

from django.urls import path
from routes.mountains import views


urlpatterns = [
    path('ridges/', views.ridges, name="ridges"),
    path('ridge/<slug>/', views.ridge, name="ridge"),
    path('add/ridge/', views.add_ridge, name="add-ridge"),
    path('remove/ridge/<slug>/', views.remove_ridge, name="remove-ridge"),
    path('edit/ridge/<slug>/', views.edit_ridge, name="edit-ridge"),
    path('peak/<slug>/', views.peak, name="peak"),
    path('remove/summit/<slug>/', views.remove_peak, name="remove-peak"),
    path('edit/summit/<slug>/', views.edit_peak, name="edit-peak"),
    path('add/summit/ridge/<slug>/', views.add_ridge_peak, name="add-ridge-peak"),
    path('add/route/peak/<slug>/', views.add_peak_route, name="add-peak-route"),
    path('peaks/', views.peaks, name="peaks"),
    path('route/<int:route_id>/', views.route, name="route"),
    path('edit/route/<int:route_id>/', views.edit_route, name="edit-route"),
    path('remove/route/<int:route_id>/', views.remove_route, name="remove-route"),
    path('', views.routes, name="routes"),
    path('add/route/<int:route_id>/section/', views.add_route_section, name="add-route-section"),
    path('add/route/<int:route_id>/point/', views.add_route_point, name="add-route-point"),
    path('remove/route/<int:route_id>/point/<int:point_id>/',
         views.remove_route_point, name="remove-route-point"),
    path('edit/route/<int:route_id>/point/<int:point_id>/',
         views.edit_route_point, name="edit-route-point"),
    path('get/route/<int:route_id>/point/<int:point_id>/',
         views.get_route_point, name="get-route-point"),
    path('update/route/<int:route_id>/point/<int:point_id>/',
         views.update_route_point, name="update-route-point"),
    path('remove/route/<int:route_id>/section/<int:section_id>/',
         views.remove_route_section, name="remove-route-section"),
    path('edit/route/<int:route_id>/section/<int:section_id>/',
         views.edit_route_section, name="edit-route-section"),
    path('get/route/<int:route_id>/section/<int:section_id>/',
         views.get_route_section, name="get-route-section"),
    path('update/route/<int:route_id>/section/<int:section_id>/',
         views.update_route_section, name="update-route-section"),
]
