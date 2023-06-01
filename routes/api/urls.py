"""
Here are all urls related to Mountain Routes API
"""

from django.urls import path, re_path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from routes.api import views


handler500 = 'rest_framework.exceptions.server_error'
handler400 = 'rest_framework.exceptions.bad_request'
handler404 = 'rest_framework.exceptions.bad_request'

schema_view = get_schema_view(
    openapi.Info(
        title="Mountain Routes API",
        default_version='v1',
        description="API for Carpathian mountain winter routes",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="aleksandr.kostin@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('hello/', views.hello_world, name='hello'),
    path('ridges/', views.RidgeList.as_view(), name='ridges'),
    path('ridges/new/', views.RidgeNew.as_view(), name='new-ridge'),
    path(
        'ridge/<slug:slug>/', views.RidgeDetail.as_view(),
        name='ridge-by-slug'),

    # implemented end-points

    # JWT autorization
    path(
        'jwt/token/', views.CustomTokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path(
        'jwt/token/refresh/', TokenRefreshView.as_view(),
        name='token_refresh'),
    path(
        'jwt/token/verify/', TokenVerifyView.as_view(),
        name='token_verify'),
    path('jwt/logout/', views.user_jwt_logout, name='api-jwt-logout'),

]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token)
]

