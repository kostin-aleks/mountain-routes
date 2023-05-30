"""
Here are all urls related to Mountain Routes API
"""

from django.urls import path, re_path
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
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('hello/', views.hello_world, name='hello'),
    # path('countries/', views.countries, name='countries'),
    # path('country/<int:country_id>/',
    # views.country, name='country-by-id'),
    #path('country/<iso>/', views.country_by_iso, name='country-by-iso'),
    #path('cities/', views.cities, name='cities'),
    #path('city/<int:city_id>/', views.city, name='city-by-id'),
    # path('country/cities/<int:country_id>/',
    # views.country_cities, name='country-cities-by-id'),
    # path('country/cities/iso/<country_iso>/',
    # views.country_cities_by_iso, name='country-cities-by-iso'),
    #path('games/', views.future_games, name='future-games'),
    # path(
    # 'regulations/<int:reglament_id>/',
    # views.regulations_by_id, name='single-regulations'),
    #path('locations/', views.locations, name='locations'),
    # path('location/tasks/<uuid:location_uuid>/',
    # views.location_tasks, name='location-tasks'),
    #path('players/', views.players, name='players'),
    #path('games/list/', views.games, name='games-list'),
    #path('game/<uuid:game_uuid>/', views.game, name='game'),
    # path('author/<int:player_id>/',
    # views.author_profile, name='author_profile'),
    #path('get/languages/', views.get_languages, name='get-languages'),
    # path('get/all/tasks/<uuid:game_uuid>/',
    # views.get_all_game_tasks, name='get-all-game-tasks'),
    #path('pay/game/', views.pay_game, name='pay-game'),
    # path('payments/game/<uuid:game_uuid>/',
    # views.payments_for_game, name='payments-for-game'),
    # path(
    # 'author/game/items/count/<uuid:game_uuid>/',
    # views.game_items_count, name='game-items-count'),
    #path('authors/', views.authors, name='authors'),
    #path('game/<uuid:game_uuid>/hints/', views.game_hints, name='game-hints'),
    #path('game/<uuid:game_uuid>/hints/<slug:destination>/', views.game_hints, name='game-hints'),

    # implemented end-points

    # JWT autorization
    # path(
    #'jwt/token/', views.CustomTokenObtainPairView.as_view(),
    # name='token_obtain_pair'),
    # path(
    # 'jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('jwt/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    #path('jwt/logout/', views.user_jwt_logout, name='api-jwt-logout'),
    # path('jwt/token/google/', views.jwt_by_google_token,
    # name='api-jwt-google-token'),

    #path('app/version/<app_slug>/', views.app_version, name='user-app-version'),
    # path(
    # 'player/auth/session/',
    # views.player_session, name='api-player-session'),
    # path(
    # 'player/auth/session/force/',
    # views.player_force_session, name='api-player-force-session'),
    # path(
    # 'player/games/<game_uuid>/',
    # views.game_full_data, name='api-game-data'),
    #path('player/games/', views.player_games, name='player-games'),
    # path('player/games/<uuid:game_uuid>/start/',
    # views.player_start_game, name='player-start-game'),
    # path('player/profile/',
    # views.player_profile, name='player-profile'),
    # path(
    # 'player/task/<uuid:uuid>/photo/',
    # views.PhotoUploadView.as_view(), name='upload-task-photo'),
    # path(
    #'player/task/<uuid:uuid>/visit/', views.visit_game_location,
    # name='visit-game-location'),
    # path(
    #'player/task/<uuid:uuid>/quest/', views.complete_quest,
    # name='complete-quest'),
    # path(
    #'player/team/<team_id>/attempts/', views.team_attempts,
    # name='team-attempts'),

]

urlpatterns += [
    path('api-token-auth/', obtain_auth_token)
]

