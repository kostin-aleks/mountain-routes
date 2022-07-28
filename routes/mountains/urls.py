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
    path('', views.routes, name="routes"),
]
