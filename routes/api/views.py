"""
Mountain Routes API end-points
"""
from datetime import datetime
from pprint import pprint
import json
import os
import requests
import sys
import uuid
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes)
from rest_framework.exceptions import AuthenticationFailed, Throttled
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateAPIView,
    ListAPIView, RetrieveAPIView
)
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.contrib.auth import get_user_model
from django.utils import timezone, translation
from django.utils.translation import gettext_lazy as _
#from country.models import Country
#from city.models import City
#from game.models import (
    #Game, GameCalculationType, Regulation, Classifier, Transport)
#from location.models import (Location, LocationType)
#from task.models import (
    #Task, TaskAttempt, TaskAttemptPhoto,
    #TaskType, TaskAttemptQuestAnswers)
#from team.models import Team
#from fcuser.models import UserProfile, UserLocation, HEADERS
#from fcuser.pipeline import get_unique_random_name, update_user_photo
#from geopoint.models import GeoPoint
from routes.api.models import App, AppVersion, UserAppVersion
#from payment.models import Payment
#from utils import (
    #get_object_or_none, user_profile, base64_to_string, decode_field,
    #get_team_or_none, get_team_or_404)
from routes.api import serializers
# from flashcross.decorators import verified_session, expert


def error_response(errors):
    """
    format response object for validation errors
    """
    items = []
    for k, v in errors.items():
        items.append('%s: %s' % (k, '; '.join(v)))
    return {
        "error": {
            "descriptions": items
        }
    }


@extend_schema(
    methods=['get'],
    responses={200: serializers.StatusSerializer},
    operation_id="Hello",
    description='GET hello/')
@api_view(['GET'])
def hello_world(request):
    """
    test api method
    """
    return Response({
        'status': 'OK',
        "message": "Hello, world!"})


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.CountrySerializer},
    #operation_id="Countries",
    #description='GET countries/')
#@api_view(['GET'])
#def countries(request):
    #"""
    #List of countries
    #"""
    #countries = Country.objects.filter(active=True)

    #return Response(
        #serializers.CountrySerializer(countries, many=True).data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.CountrySerializer},
    #operation_id="Country",
    #description='GET country/{country_id}/')
#@api_view(['GET'])
#def country(request, country_id):
    #"""
    #Country by id
    #"""
    #country = get_object_or_none(Country, pk=country_id)
    #if country is None:
        #return Response({}, status=status.HTTP_400_BAD_REQUEST)

    #return Response(serializers.CountrySerializer(country).data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.CountrySerializer},
    #operation_id="Country by ISO",
    #description='GET country/{iso}/')
#@api_view(['GET'])
#def country_by_iso(request, iso):
    #"""
    #Country by iso
    #"""
    #country = get_object_or_none(Country, iso=iso)
    #if country is None:
        #return Response({}, status=status.HTTP_400_BAD_REQUEST)

    #return Response(serializers.CountrySerializer(country).data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.CitySerializer},
    #operation_id="Cities",
    #description='GET cities/')
#@api_view(['GET'])
#def cities(request):
    #"""
    #List of cities
    #"""
    #cities = City.objects.filter(active=True).order_by('country', 'name')
    #return Response(
        #serializers.CitySerializer(cities, many=True).data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.CitySerializer},
    #operation_id="Country's cities",
    #description='GET country/cities/{country_id}/')
#@api_view(['GET'])
#def country_cities(request, country_id):
    #"""
    #list of country cities
    #"""
    #country = get_object_or_none(Country, pk=country_id)
    #if country is None:
        #return Response({}, status=status.HTTP_400_BAD_REQUEST)
    #cities = country.city_set.filter(active=True)

    #serializer = serializers.CitySerializer(cities, many=True)
    #return Response(serializer.data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.CitySerializer},
    #operation_id="Country's cities by country iso",
    #description='GET country/cities/iso/{country_iso}/')
#@api_view(['GET'])
#def country_cities_by_iso(request, country_iso):
    #"""
    #list of country cities by country ISO
    #"""
    #country = get_object_or_none(Country, iso=country_iso.upper())
    #if country is None:
        #return Response({}, status=status.HTTP_400_BAD_REQUEST)
    #cities = country.city_set.filter(active=True)

    #serializer = serializers.CitySerializer(cities, many=True)
    #return Response(serializer.data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.CitySerializer},
    #operation_id="City",
    #description='GET city/{city_id}/')
#@api_view(['GET'])
#def city(request, city_id):
    #"""
    #City by id
    #"""
    #city = get_object_or_none(City, pk=city_id)
    #if city is None:
        #return Response({}, status=status.HTTP_400_BAD_REQUEST)

    #return Response(serializers.CitySerializer(city).data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.GameSerializer},
    #operation_id="Games",
    #description='GET future/games/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def future_games(request):
    #"""
    #List of future games
    #"""
    #games = Game.objects.all()
    #games = games.exclude(archived=True)
    #games = games.exclude(deadline__lt=timezone.now())
    #games = games.exclude(finish__lt=timezone.now())

    #return Response(
        #serializers.GameSerializer(games, many=True).data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.RegulationSerializer},
    #operation_id="Regulations",
    #description='GET author/regulations')
#@api_view(['GET'])
#def regulations(request):
    #"""
    #List of regulations
    #"""
    #regulations = Regulation.objects.all()

    #return Response(
        #serializers.RegulationSerializer(regulations, many=True).data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.TransportInfoSerializer},
    #operation_id="Transport",
    #description='GET author/transports')
#@api_view(['GET'])
#def transports(request):
    #"""
    #List of transports
    #"""
    #transports = Transport.objects.all()

    #return Response(
        #serializers.TransportInfoSerializer(transports, many=True).data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.ClassifierInfoSerializer},
    #operation_id="Classifier",
    #description='GET author/classifiers')
#@api_view(['GET'])
#def classifiers(request):
    #"""
    #List of classifiers
    #"""
    #classifiers = Classifier.objects.all()

    #return Response(
        #serializers.ClassifierInfoSerializer(classifiers, many=True).data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.CalculationTypeInfoSerializer},
    #operation_id="Calculation Type",
    #description='GET author/calculation/types/')
#@api_view(['GET'])
#def calculation_types(request):
    #"""
    #List of calculation types
    #"""
    #types = GameCalculationType.objects.all()

    #return Response(
        #serializers.CalculationTypeInfoSerializer(types, many=True).data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.RegulationSerializer},
    #operation_id="The regulations",
    #description='GET regulations/{reglament_id}/')
#@api_view(['GET'])
#def regulations_by_id(request, reglament_id):
    #"""
    #Regulations by id
    #"""
    #regulations = get_object_or_none(Regulation, pk=reglament_id)
    #if regulations is None:
        #return Response({}, status=status.HTTP_400_BAD_REQUEST)

    #return Response(serializers.RegulationSerializer(regulations).data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.LocationSerializer},
    #operation_id="Locations",
    #description='GET locations/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def locations(request):
    #"""
    #List of locations
    #"""
    #return Response(
        #serializers.LocationSerializer(
            #Location.objects.order_by('created'), many=True).data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.AuthorLocationFullDataSerializer},
    #operation_id="Location",
    #description='GET location/{location_uuid}/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def location(request, location_uuid):
    #"""
    #get a single Location
    #"""
    #author = request.user.userprofile

    #location = get_object_or_404(Location, pk=location_uuid)

    #if location.game is None:
        #return Response(
            #{'error': _('The location must be related to the game')},
            #status=status.HTTP_403_FORBIDDEN)
    #if not location.game.is_author(author.user):
        #return Response(
            #{'error': _('The user must be the author of this game')},
            #status=status.HTTP_403_FORBIDDEN)

    #data = serializers.AuthorLocationFullDataSerializer(location).data

    #return Response(data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.TaskDataSerializer},
    #operation_id="Task",
    #description='GET task/{task_uuid}/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def task(request, task_uuid):
    #"""
    #get a single Task
    #"""
    #task = get_object_or_404(Task, pk=task_uuid)
    #author = request.user.userprofile
    #if not task.game.is_author(author.user):
        #return Response(
            #{'error': _('The user must be the author of this game')},
            #status=status.HTTP_403_FORBIDDEN)
    #data = serializers.TaskDataSerializer(task).data

    #return Response(data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.AppVersionSerializer},
    #operation_id='Get application version',
    #description='POST app/version/{app_slug}/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def app_version(request, app_slug):
    #"""
    #gets newest app version and stores user application information
    #"""
    #application = get_object_or_404(App, slug=app_slug)
    #version = AppVersion.newest_version(app_slug)

    #UserAppVersion.objects.create(
        #app=application,
        #user=request.user,
        #user_app_version=request.headers.get(HEADERS.APP_VERSION),
        #app_version=version,
        #device=request.headers.get(HEADERS.DEVICE),
        #os=request.headers.get(HEADERS.OS))

    #return Response(serializers.AppVersionSerializer(
        #{
            #'application': application.name,
            #'slug': application.slug,
            #'version': version.version,
            #'author': version.author,
            #'created': version.created
        #}).data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.GameLocationsSerializer},
    #operation_id="Game locations",
    #description='GET game/locations/{game_uuid}/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def game_locations(request, game_uuid):
    #"""
    #list of game locations
    #"""
    #game = get_object_or_404(Game, pk=game_uuid)
    #author = request.user.userprofile

    #if not game.is_author(author.user):
        #return Response(
            #{'error': _('The user must be the author of this game')},
            #status=status.HTTP_403_FORBIDDEN)

    #locations = game.location_set.all()

    #serializer = serializers.GameLocationsSerializer(
        #{'locations': locations, 'game_uuid': game.uuid})
    #data = serializer.data

    #return Response(data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.PlayersSerializer},
    #operation_id='Players',
    #description='GET players/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def players(request):
    #"""
    #list of players
    #"""
    #players = get_user_model().objects.all()

    #serializer = serializers.PlayersSerializer({'players': players})
    #return Response(serializer.data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.PlayerSerializer},
    #operation_id='Player by id',
    #description='GET player/{player_id}/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def player(request, pk):
    #"""
    #player's information
    #"""
    #player = user_profile(pk)
    #serializer = serializers.PlayerSerializer(player.as_dictionary)

    #return Response(serializer.data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.PlayerGamesSerializer},
    #operation_id='Games of the player',
    #description='GET player/games/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def player_games(request):
    #"""
    #player games list
    #"""
    #set_language(request.headers)
    #player = request.user.userprofile
    #games = player.player_games_as_list(request)
    #serializer = serializers.PlayerGamesSerializer(
        #{'result': games})

    #return Response(serializer.data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.PlayerTeamsSerializer},
    #operation_id='Teams of the player',
    #description='GET player/teams/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def player_teams(request):
    #"""
    #player teams list
    #"""
    #player = request.user.userprofile
    #serializer = serializers.PlayerTeamsSerializer(
        #{
            #'player_id': player.user.id,
            #'teams_list': player.teams()})

    #return Response(serializer.data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.GamesSerializer},
    #operation_id='Games',
    #description='GET games/list/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def games(request):
    #"""
    #list of games
    #"""
    #player = request.user.userprofile
    #games = Game.objects.all()
    #games = games.order_by('created')
    #if not request.GET.get('all', False):
        #games = games.exclude(archived=True)
    #games = [
        #{
            #'short_name': game.short_name,
            #'uuid': game.uuid,
            #'city': game.city,
            #'country': game.country,
            #'participation': game.participation_in_game(player),
            #'start': game.start.date() if game.start else None}
        #for game in games]
    #serializer = serializers.GamesSerializer(
        #{
            #'games': games})

    #return Response(serializer.data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.GameDetailedSerializer},
    #operation_id='Game',
    #description='GET game/{game_uuid}/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def game(request, game_uuid):
    #"""
    #the game information
    #"""
    #player = request.user.userprofile
    #game = get_object_or_404(Game, pk=game_uuid)
    #serializer = serializers.GameDetailedSerializer(
        #{
            #'game': game,
            #'player': player.id,
            #'participation': game.participation_in_game(player),
            #'country': game.country.name,
            #'city': game.city.name,
        #})
    #return Response(serializer.data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.AuthorProfileSerializer},
    #operation_id="Author's profile",
    #description='GET author/{player_id}/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def author_profile(request, player_id):
    #"""
    #author profile
    #"""
    #author = user_profile(player_id)

    #serializer = serializers.AuthorProfileSerializer(author.author_profile)
    #return Response(serializer.data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.LocationTaskListSerializer},
    #operation_id='Location tasks',
    #description='GET location/tasks/{location_uuid}/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def location_tasks(request, location_uuid):
    #"""
    #location's tasks
    #"""
    #player = request.user.userprofile
    #location = get_object_or_404(Location, uuid=location_uuid)

    #serializer = serializers.LocationTaskListSerializer(
        #{
            #'game_uuid': location.game.uuid,
            #'location_uuid': location.uuid,
            #'tasks_list': location.tasks
        #})

    #return Response(serializer.data)


#class PhotoUploadView(APIView):
    #"""
    #send task photo of the team
    #"""
    #permission_classes = [IsAuthenticated]
    #parser_class = (FileUploadParser, )

    #@extend_schema(
        #request=serializers.CompleteTaskSerializer,
        #responses={201: serializers.SuccessSerializer},
        #operation_id='Upload team task photo',
        #description='POST player/task/{uuid}/photo/')
    #def post(self, request, uuid, *args, **kwargs):
        #"""
        #overrided method
        #creates new photo or updates existent one
        #"""
        #fmt = '%Y-%b-%d %H:%M:%S %Z %z'
        #set_language(request.headers)

        #task = get_object_or_404(Task, pk=uuid)
        #game = task.game
        #player = request.user.userprofile
        #team = player.game_team(game)

        #serializer = serializers.CompleteTaskSerializer(data=request.data)

        #if not serializer.is_valid():
            #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #if not player.verified_session(request.headers.get('X-Session-ID')):
            #raise Throttled(detail=_('Not valid session ID'))

        #if not team.has_player(request.user):
            #return Response({}, status=status.HTTP_403_FORBIDDEN)

        #post_data = serializer.data
        #point = None

        #if post_data.get('lat') and post_data.get('lon'):
            #point = GeoPoint.objects.create(
                #latitude=post_data['lat'],
                #longitude=post_data['lon'])

        #completed = not post_data['need_verification']
        #dt = post_data.get('timestamp') or timezone.now()

        #data = {
            #'photo': request.data.get('image'),
            #'team': team.id,
            #'task': task.uuid
        #}

        #serializer = serializers.TaskAttemptPhotoSerializer(data=data)

        #if serializer.is_valid() and team.has_player(player.user) \
                #and team.started():
            #photo = serializer.save()

            #completed_task = task.complete(
                #team, player, point, dt, completed)

            #set_attempt_telemetry(photo, post_data)

            #photo.taskattempt = completed_task
            #photo.player = player.user

            #photo.found_points = post_data.get('found_points')
            #algorithm_parameters = post_data.get(
                #'algorithm_parameters')
            #if algorithm_parameters is not None:
                #algorithm_parameters = json.loads(algorithm_parameters)
            #photo.algorithm_parameters = algorithm_parameters

            #algorithm_telemetry = post_data.get(
                #'algorithm_telemetry')
            #if algorithm_telemetry is not None:
                #algorithm_telemetry = json.loads(algorithm_telemetry)
            #photo.algorithm_telemetry = algorithm_telemetry

            #photo.save()

            #return Response({'success': True}, status=status.HTTP_201_CREATED)
        #else:
            #return Response(
                #{'success': False}, status=status.HTTP_400_BAD_REQUEST)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.CountrySerializer},
    #operation_id='Country by iso',
    #description='GET countries/{iso}/')
#@api_view(['GET'])
#def country_by_iso(request, iso):
    #"""
    #get country by iso
    #"""
    #country = get_object_or_404(Country, iso=iso.upper())
    #serializer = serializers.CountrySerializer(country)

    #return Response(serializer.data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.LanguagesSerializer},
    #operation_id='Get languages',
    #description='GET get/languages/')
#@api_view(['GET'])
#def get_languages(request):
    #"""
    #get list of languages
    #"""
    #languages = [{'code': x[0], 'name': x[1]} for x in settings.LANGUAGES]
    #serializer = serializers.LanguagesSerializer({'languages': languages})

    #return Response(serializer.data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.GameTasksSerializer},
    #operation_id='Get all tasks of the game',
    #description='GET get/all/tasks/{game_uuid}/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def get_all_game_tasks(request, game_uuid):
    #"""
    #get all game tasks
    #"""
    #player = request.user.userprofile
    #game = get_object_or_404(Game, pk=game_uuid)
    #team = player.game_team(game)

    #serializer = serializers.GameTasksSerializer(
        #{'locations': game.all_tasks()})

    #if game.is_author(request.user):
        #return Response(serializer.data)

    #if player.plays(game) and game.team_paid_participation(team):
        #return Response(serializer.data)

    #return Response({}, status=status.HTTP_403_FORBIDDEN)


#@extend_schema(
    #methods=['post'],
    #request=serializers.PaymentSerializer,
    #responses={200: serializers.StatusSerializer},
    #operation_id='Pay game',
    #description='POST pay/game/')
#@api_view(['POST'])
#@permission_classes([IsAuthenticated])
#def pay_game(request):
    #"""
    #store team payment for the game
    #"""
    #serializer = serializers.PaymentSerializer(data=request.data)

    #if not serializer.is_valid():
        #return Response({}, status=status.HTTP_400_BAD_REQUEST)

    #data = serializer.data
    #game = get_object_or_404(Game, uuid=data['game_uuid'])
    #player = request.user.userprofile
    #team = get_team_or_404(Team, id=data['team_id'])

    #if team.game == game:
        #Payment.objects.create(
            #game=game,
            #team=team,
            #user=player.user,
            #amount=data['amount'],
        #)
        #return Response({'status': 'OK'})

    #return Response({}, status=status.HTTP_400_BAD_REQUEST)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.GamePaymentsSerializer},
    #operation_id='Team game payments',
    #description='GET payments/game/{uuid:game_uuid}/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def payments_for_game(request, game_uuid):
    #"""
    #team's payments for the game
    #"""
    #player = request.user.userprofile
    #game = get_object_or_404(Game, uuid=game_uuid)
    #team = player.game_team(game)
    #payments = Payment.objects.filter(game=game, team=team).order_by('id')

    #serializer = serializers.GamePaymentsSerializer({'payments': payments})

    #return Response(serializer.data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.PlayerProfileSerializer},
    #operation_id='Player profile',
    #description='GET player/profile/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#@verified_session
#def player_profile(request):
    #"""
    #player's profile
    #"""
    #set_language(request.headers)
    #serializer = serializers.PlayerProfileSerializer(
        #request.user.userprofile.player_profile(mine=True, request=request))

    #return Response(serializer.data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.AuthorGamesSerializer},
    #operation_id='Games of the author',
    #description='GET author/games/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def author_games(request):
    #"""
    #author games list
    #"""
    #author = request.user.userprofile
    #games = author.author_games_as_list()

    #serializer = serializers.AuthorGamesSerializer(
        #{
            #'author_id': author.user.id,
            #'games': games})

    #data = serializer.data

    #return Response(serializer.data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.GameItemsCountSerializer},
    #operation_id='Count of locations for the game',
    #description='GET author/items/count/{game_uuid}/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def game_items_count(request, game_uuid):
    #"""
    #returns count of game locations for the game
    #"""
    #author = request.user.userprofile
    #game = get_object_or_404(Game, pk=game_uuid)

    #if not game.is_author(author.user):
        #return Response({}, status=status.HTTP_400_BAD_REQUEST)

    #serializer = serializers.GameItemsCountSerializer(
        #{
            #'game': game,
            #'locations_count': game.locations().count(),
            #'tasks_count': game.active_tasks().count(),
        #})

    #return Response(serializer.data)


#@extend_schema(
    #methods=['post'],
    #request=serializers.AddLocationSerializer,
    #responses={201: serializers.StatusSerializer},
    #operation_id='Add new game location',
    #description='POST author/add/location/{game_uuid}/')
#@api_view(['POST'])
#@permission_classes([IsAuthenticated])
#def game_add_location(request, game_uuid):
    #"""
    #add new game location
    #"""
    #serializer = serializers.AddLocationSerializer(data=request.data)

    #if not serializer.is_valid():
        #return Response(
            #error_response(serializer.errors),
            #status=status.HTTP_400_BAD_REQUEST)

    #data = serializer.data

    #game = get_object_or_404(Game, pk=game_uuid)
    #location_type = get_object_or_404(LocationType, slug=data['location_type'])
    #author = request.user.userprofile

    #if not game.is_author(author.user):
        #return Response(
            #{'error': _('The user must be the author of this game')},
            #status=status.HTTP_403_FORBIDDEN)

    #location_uuid = data.get('uuid')
    #if location_uuid is None:
        #location_uuid = str(uuid.uuid4())

    #location = get_object_or_none(Location, pk=location_uuid)
    #if location:
        #return Response(
            #{'status': 'OK', 'id': location.uuid},
            #status=status.HTTP_200_OK)

    #location = Location(
        #uuid=location_uuid,
        #game=game,
        #name=data['name'],
        #short_name=data['short_name'],
        #location_type=location_type,
        #description=data.get('description', ''),
        #start_minutes=data.get('start_minutes', 0),
        #finish_minutes=data.get('finish_minutes', 0),
        #radius=data.get('radius', 0),
        #number=data['number'],
        #hint=data.get('hint', ''),
        #visible=data.get('visible', True),
        #finish=data.get('finish', False),
        #active=data.get('active', True),
    #)
    #if data.get('latitude') and data.get('longitude'):
        #point = GeoPoint.objects.create(
            #latitude=data['latitude'],
            #longitude=data['longitude']
        #)
        #location.point = point
        #location.game.update_rectangle()

    #location.save()

    #location.author = author.user
    #location.save()

    ## location.add_visitable_task()

    #return Response(
        #{'status': 'OK', 'id': location.uuid},
        #status=status.HTTP_201_CREATED)


#class LocationPhotoUploadView(APIView):
    #"""
    #upload location photo
    #"""
    #permission_classes = [IsAuthenticated]
    #parser_class = (FileUploadParser, )

    #@extend_schema(
        #request=serializers.LocationPhotoSerializer,
        #responses={201: serializers.StatusSerializer},
        #operation_id='Upload location photo',
        #description='POST author/upload/location/photo/')
    #def post(self, request, *args, **kwargs):
        #"""
        #overrided method
        #creates new photo or updates existent one
        #"""
        #location = get_object_or_404(
            #Location, pk=request.data.get('uuid'))

        #if not location.game.is_author(request.user):
            #return Response(
                #{'error': _('The user must be the author of this game')},
                #status=status.HTTP_403_FORBIDDEN)

        #serializer = serializers.LocationPhotoSerializer(
            #location, data=request.data)

        #if serializer.is_valid():
            #serializer.save()
            #return Response({'status': 'OK'}, status=status.HTTP_201_CREATED)
        #else:
            #return Response(
                #error_response(serializer.errors),
                #status=status.HTTP_400_BAD_REQUEST)


#@extend_schema(
    #methods=['post'],
    #request=serializers.UpdateLocationSerializer,
    #responses={201: serializers.StatusSerializer},
    #operation_id='Update the game location',
    #description='POST author/update/location/{location_uuid}/')
#@api_view(['POST'])
#@permission_classes([IsAuthenticated])
#def game_update_location(request, location_uuid):
    #"""
    #update the game location
    #"""
    #request_data = request.data
    #serializer = serializers.UpdateLocationSerializer(data=request.data)

    #if not serializer.is_valid():
        #return Response(
            #error_response(serializer.errors),
            #status=status.HTTP_400_BAD_REQUEST)

    #data = serializer.data

    #location = get_object_or_404(Location, pk=location_uuid)
    #author = request.user.userprofile

    #if not location.game.is_author(author.user):
        #return Response(
            #{'error': _('The user must be the author of this game')},
            #status=status.HTTP_403_FORBIDDEN)

    #if 'name' in request_data:
        #location.name = data['name']
    #if 'short_name' in request_data:
        #location.short_name = data['short_name']
    #if 'location_type' in request_data:
        #location_type = get_object_or_404(
            #LocationType, slug=data['location_type'])
        #location.location_type = location_type
    #if 'description' in request_data:
        #location.description = data.get('description', '')
    #if 'hint' in request_data:
        #location.hint = data.get('hint', '')
    #if 'number' in request_data:
        #location.number = data.get('number')
    #if 'start_minutes' in request_data:
        #location.start_minutes = data.get('start_minutes')
    #if 'finish_minutes' in request_data:
        #location.finish_minutes = data.get('finish_minutes')
    #if 'radius' in request_data:
        #location.radius = data.get('radius')
    #if 'visible' in request_data:
        #location.visible = data.get('visible')
    #if 'finish' in request_data:
        #location.finish = data.get('finish')
    #if 'active' in request_data:
        #location.active = data.get('active')

    #if 'latitude' in request_data and 'longitude' in request_data:
        #if data.get('latitude') and data.get('longitude'):
            #if location.point is None:
                #point = GeoPoint.objects.create(
                    #latitude=data['latitude'],
                    #longitude=data['longitude']
                #)
                #location.point = point
            #else:
                #location.point.latitude = data['latitude']
                #location.point.longitude = data['longitude']
                #location.point.save()
        #else:
            #location.point = None

    #location.save()

    #return Response(
        #{'status': 'OK', 'uuid': location.uuid},
        #status=status.HTTP_201_CREATED)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.LocationTypesSerializer},
    #operation_id='List of location types',
    #description='GET location/types/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def location_types(request):
    #"""
    #list of location types
    #"""
    #serializer = serializers.LocationTypesSerializer(
        #{'types': LocationType.objects.order_by('id')})

    #return Response(serializer.data)


#def remove_task(task):
    #"""
    #remove task and related objects
    #"""
    #task.game = None
    #task.location = None
    #task.author = None
    #task.save()


#@extend_schema(
    #methods=['post'],
    #responses={200: serializers.StatusSerializer},
    #operation_id='Remove game location',
    #description='POST author/remove/location/{location_uuid}/')
#@api_view(['POST'])
#@permission_classes([IsAuthenticated])
#def game_remove_location(request, location_uuid):
    #"""
    #remove the game location
    #"""
    #author = request.user.userprofile

    #location = get_object_or_404(Location, pk=location_uuid)

    #game = location.game
    #if game and game.status_new():
        #if not location.game.is_author(author.user):
            #return Response(
                #{'error': _('The user must be the author of this game')},
                #status=status.HTTP_403_FORBIDDEN)

        #location.game = None
        #location.author = None
        #location.save()

        #for task in location.task_set.all():
            #remove_task(task)

    #return Response({'status': 'OK'}, status=status.HTTP_200_OK)


#@extend_schema(
    #methods=['post'],
    #responses={200: serializers.StatusSerializer},
    #operation_id='Remove game task',
    #description='POST author/remove/task/{task_uuid}/')
#@api_view(['POST'])
#@permission_classes([IsAuthenticated])
#def game_remove_task(request, task_uuid):
    #"""
    #remove the game task
    #"""
    #author = request.user.userprofile
    #task = get_object_or_404(Task, pk=task_uuid)

    #game = task.game
    #if game and game.status_new():
        #if not task.game.is_author(author.user):
            #return Response({}, status=status.HTTP_403_FORBIDDEN)

        #remove_task(task)

    #return Response({'status': 'OK'})


#@extend_schema(
    #methods=['post'],
    #request=serializers.AddTaskSerializer,
    #responses={200: serializers.StatusSerializer},
    #operation_id='Add new game task',
    #description='POST author/add/task/{location_uuid}/')
#@api_view(['POST'])
#@permission_classes([IsAuthenticated])
#def game_add_task(request, location_uuid):
    #"""
    #add new game task
    #"""
    #serializer = serializers.AddTaskSerializer(data=request.data)

    #if not serializer.is_valid():
        #return Response(
            #error_response(serializer.errors),
            #status=status.HTTP_400_BAD_REQUEST)

    #data = serializer.data

    #location = get_object_or_404(Location, pk=location_uuid)
    #task_type = get_object_or_404(TaskType, slug=data['task_type'])
    #author = request.user.userprofile

    #if not location.game.is_author(author.user):
        #return Response({}, status=status.HTTP_403_FORBIDDEN)

    #task_uuid = data.get('uuid')
    #if task_uuid is None:
        #task_uuid = str(uuid.uuid4())

    #task = get_object_or_none(Task, pk=task_uuid)
    #if task:
        #return Response({
            #'status': 'OK',
            #'id': task.uuid,
        #})

    #task = Task(
        #uuid=task_uuid,
        #game=location.game,
        #location=location,
        #num=data['num'],
        #author=author.user,
        #task_type=task_type,
        #text=data.get('text', ''),
        #hint=data.get('hint', ''),
        #answers=data.get('answers', ''),
        #base_score=data.get('base_score', 0),
        #difficulty=data.get('difficulty'),
        #visible=data.get('visible', 'everywhere'),
        #doable=data.get('doable', 'everywhere'),
        #enterable=data.get('enterable', 'everywhere'),
        #radius=data.get('radius', 100),
        #algorithm_points=data.get('algorithm_points'),
        #algorithm_distance=data.get('algorithm_distance'),
        #active=data.get('active', True),
    #)

    #if data.get('latitude') and data.get('longitude'):
        #point = GeoPoint.objects.create(
            #latitude=data['latitude'],
            #longitude=data['longitude']
        #)
        #task.point = point

    #task.save()

    #return Response({
        #'status': 'OK',
        #'id': task.uuid,
    #})


#@extend_schema(
    #methods=['post'],
    #request=serializers.UpdateTaskSerializer,
    #responses={200: serializers.StatusSerializer},
    #operation_id='Update the game task',
    #description='POST author/update/task/{task_uuid}/')
#@api_view(['POST'])
#@permission_classes([IsAuthenticated])
#def game_update_task(request, task_uuid):
    #"""
    #update the game task
    #"""
    #request_data = request.data
    #serializer = serializers.UpdateTaskSerializer(data=request.data)

    #if not serializer.is_valid():
        #return Response(
            #error_response(serializer.errors),
            #status=status.HTTP_400_BAD_REQUEST)

    #data = serializer.data

    #task = get_object_or_404(Task, pk=task_uuid)
    #author = request.user.userprofile

    #if not task.game.is_author(author.user):
        #return Response({}, status=status.HTTP_403_FORBIDDEN)

    #if 'num' in request_data:
        #task.num = data['num']
    #if 'task_type' in request_data:
        #task_type = get_object_or_404(TaskType, slug=data['task_type'])
        #task.task_type = task_type
    #if 'text' in request_data:
        #task.text = data.get('text', '')
    #if 'hint' in request_data:
        #task.hint = data.get('hint', '')
    #if 'answers' in request_data:
        #task.answers = data.get('answers', '')
    #if 'base_score' in request_data:
        #task.base_score = data.get('base_score')
    #if 'difficulty' in request_data:
        #task.difficulty = data.get('difficulty')
    #if 'visible' in request_data:
        #task.visible = data.get('visible', 'everywhere')
    #if 'doable' in request_data:
        #task.doable = data.get('doable', 'everywhere')
    #if 'enterable' in request_data:
        #task.enterable = data.get('enterable', 'everywhere')
    #if 'radius' in request_data:
        #task.radius = data.get('radius')
    #if 'algorithm_points' in request_data:
        #task.algorithm_points = data.get('algorithm_points')
    #if 'algorithm_distance' in request_data:
        #task.algorithm_distance = data.get('algorithm_distance')
    #if 'active' in request_data:
        #task.active = data.get('active')

    #if 'latitude' in request_data and 'longitude' in request_data:
        #if data.get('latitude') and data.get('longitude'):
            #if task.point is None:
                #point = GeoPoint.objects.create(
                    #latitude=data['latitude'],
                    #longitude=data['longitude']
                #)
                #task.point = point
            #else:
                #task.point.latitude = data['latitude']
                #task.point.longitude = data['longitude']
                #task.point.save()
        #else:
            #task.point = None
    #task.save()

    #return Response({
        #'status': 'OK',
        #'id': task.uuid,
    #})


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.LocationTypesSerializer},
    #operation_id='List of task types',
    #description='GET task/types/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def task_types(request):
    #"""
    #list of task types
    #"""
    #serializer = serializers.LocationTypesSerializer(
        #{'types': TaskType.objects.order_by('id')})

    #return Response(serializer.data)


#class TaskPhotoUploadView(APIView):
    #"""
    #upload task photo by author
    #"""
    #permission_classes = [IsAuthenticated]
    #parser_class = (FileUploadParser, )

    #@extend_schema(
        #request=serializers.TaskPhotoSerializer,
        #responses={201: serializers.StatusSerializer},
        #operation_id='Upload task photo',
        #description='POST author/upload/task/photo/')
    #def post(self, request, *args, **kwargs):
        #"""
        #overrided method
        #creates new photo or updates existent one
        #"""
        #task = get_object_or_404(
            #Task, pk=request.data.get('uuid'))

        #if not task.game.is_author(request.user):
            #return Response({}, status=status.HTTP_403_FORBIDDEN)

        #serializer = serializers.TaskPhotoSerializer(
            #task, data=request.data)

        #if serializer.is_valid():
            #serializer.save()
            #return Response({'status': 'OK'}, status=status.HTTP_201_CREATED)
        #else:
            #return Response(
                #error_response(serializer.errors),
                #status=status.HTTP_400_BAD_REQUEST)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.AuthorsSerializer},
    #operation_id='Authors',
    #description='GET authors/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def authors(request):
    #"""
    #list of authors
    #"""
    #authors = UserProfile.users_with_perm('fcuser.can_be_author')

    #serializer = serializers.AuthorsSerializer({'authors': authors})
    #return Response(serializer.data)


#@extend_schema(
    #methods=['post'],
    #responses={200: serializers.StatusSerializer},
    #request=serializers.TokenSerializer,
    #operation_id='Log out user',
    #description='POST jwt/logout/')
#@api_view(['POST'])
#@permission_classes([IsAuthenticated])
#def user_jwt_logout(request):
    #"""
    #log out user
    #"""
    #set_language(request.headers)

    #user = request.user
    #player = user.userprofile

    #serializer = serializers.TokenSerializer(data=request.data)
    #if not serializer.is_valid():
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #refresh_token = serializer.data.get('refresh')
    #try:
        #token = RefreshToken(refresh_token)
        #token.blacklist()
        #session = player.active_player_session()
        #if session:
            #session.delete = timezone.now()
            #session.active = False
            #session.save()
    #except TokenError:
        #return Response(
            #{'error': 'Bad refresh token'},
            #status=status.HTTP_400_BAD_REQUEST)

    #return Response({'status': 'OK'}, status=status.HTTP_200_OK)


#class CustomTokenObtainPairView(TokenObtainPairView):
    ## Replace the serializer with your custom
    #serializer_class = serializers.CustomTokenObtainPairSerializer


#def valid_google_response(data):
    #"""
    #validate key fields in response
    #"""
    #try:
        #iss = data['iss']
        #aud = data['aud']
        #verified = data['email_verified']
        #exp = data['exp']

        #if "accounts.google.com" in iss:
            #if aud == settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY:
                #if verified == 'true':
                    #exp_date = datetime.fromtimestamp(int(exp))
                    #if datetime.now() < exp_date:
                        #return True
    #except ValueError:
        #pass
    #except KeyError:
        #pass
    #return False


#def register_google_user(email, data, more_data):
    #"""
    #register new user using google data
    #"""
    #username = get_unique_random_name()
    #password = get_user_model().objects.make_random_password(length=20)
    #user = get_user_model().objects.create(
        #username=username,
        #password=password,
        #email=email)

    #profile = user.userprofile
    #profile.new = False
    #profile.google_id = data.get('sub')
    #profile.first_name = data.get('given_name')
    #profile.last_name = data.get('family_name')
    #profile.language = data.get('locale') or 'en'

    #if more_data.get('phone'):
        #phone = more_data.get('phone')
        #phone = ''.join(filter(lambda i: i.isdigit(), phone))
        #profile.phone = phone

    #if more_data.get('birthday'):
        #if len(more_data.get('birthday').split('/')):
            #profile.birthday = datetime.strptime(
                #more_data.get('birthday'), '%Y/%m/%d').date()

    #if more_data.get('gender'):
        #gender = more_data.get('gender')
        #profile.gender = 0 if gender == 'male' else 1

    #profile.save()

    #picture = data.get('picture')
    #if picture:
        #update_user_photo(profile, picture)

    #return user


#@extend_schema(
    #methods=['post'],
    #responses={200: serializers.TokenPairSerializer},
    #request=serializers.GoogleTokenSerializer,
    #operation_id='Token by google token',
    #description='POST jwt/token/google/')
#@api_view(['POST'])
#def jwt_by_google_token(request):
    #"""
    #get token by google id_token
    #"""
    #serializer = serializers.GoogleTokenSerializer(data=request.data)
    #if not serializer.is_valid():
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #req_data = serializer.data
    #response = requests.get(
        #'https://oauth2.googleapis.com/tokeninfo?id_token={}'.format(
            #req_data['token']))
    #data = json.loads(response.content)
    #email = data.get('email')

    #if not email:
        #return Response(
            #{'error': 'no email'}, status=status.HTTP_404_NOT_FOUND)

    #if email and valid_google_response(data):
        #new_user = False
        #user = get_user_model().objects.filter(email=email).first()
        #if req_data.get('register'):
            #if user is None:
                #user = register_google_user(email, data, req_data)
                #new_user = True
        #if user:
            #refresh = RefreshToken.for_user(user)
            #serializer = serializers.TokenPairSerializer({
                #'superuser': user.is_superuser,
                #'refresh': str(refresh),
                #'access': str(refresh.access_token),
                #'jti': str(refresh.get('jti')),
            #})
            #response_status = status.HTTP_200_OK
            #if new_user:
                #response_status = status.HTTP_201_CREATED
            #return Response(serializer.data, status=response_status)
        #else:
            #return Response(
                #{'error': 'user not found'}, status=status.HTTP_401_UNAUTHORIZED)
    #return Response(
        #{'error': 'invalid id_token'}, status=status.HTTP_400_BAD_REQUEST)


#@extend_schema(
    #methods=['post'],
    #responses={200: serializers.PlayerSessionsSerializer},
    #request=serializers.UUIDSerializer,
    #operation_id='Player session',
    #description='POST player/auth/session/')
#@api_view(['POST'])
#@permission_classes([IsAuthenticated])
#def player_session(request):
    #"""
    #create or update player session
    #"""
    #set_language(request.headers)
    #player = request.user.userprofile

    #serializer = serializers.UUIDSerializer(data=request.data)

    #if not serializer.is_valid():
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #uuid = serializer.data.get('uuid')

    #other_sessions = player.other_sessions(uuid)
    #if not other_sessions:
        #session = player.get_or_create_session(uuid, request.headers)
        #serializer = serializers.UUIDSerializer({'uuid': session.id})
        #return Response(serializer.data, status=status.HTTP_201_CREATED)
    #else:
        #serializer = serializers.PlayerSessionsSerializer(
            #{'sessions': other_sessions})
        #return Response(serializer.data, status=status.HTTP_200_OK)


#@extend_schema(
    #methods=['post'],
    #responses={200: serializers.UUIDSerializer},
    #request=serializers.UUIDSerializer,
    #operation_id='Player force session',
    #description='POST player/auth/session/force/')
#@api_view(['POST'])
#@permission_classes([IsAuthenticated])
#def player_force_session(request):
    #"""
    #force player session
    #"""
    #set_language(request.headers)
    #player = request.user.userprofile

    #serializer = serializers.UUIDSerializer(data=request.data)

    #if not serializer.is_valid():
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #uuid = serializer.data.get('uuid')

    #session = player.get_or_create_session(uuid, request.headers)
    #other_sessions = player.other_sessions(uuid)
    #if other_sessions:
        #for session in other_sessions:
            #session.delete = timezone.now()
            #session.active = False
            #session.save()
    #serializer = serializers.UUIDSerializer({'uuid': session.id})
    #return Response(serializer.data, status=status.HTTP_201_CREATED)


#@extend_schema(
    #methods=['post'],
    #request=serializers.KeywordAndPositionSerializer,
    #responses={200: serializers.ResponseStatusSerializer},
    #operation_id='Start the game',
    #description='POST player/games/{game_uuid}/start/')
#@api_view(['POST'])
#@permission_classes([IsAuthenticated])
#@verified_session
#def player_start_game(request, game_uuid):
    #"""
    #start the game for the team by the keyword
    #"""
    #set_language(request.headers)
    #serializer = serializers.KeywordAndPositionSerializer(data=request.data)
    #if not serializer.is_valid():
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #data = serializer.data
    #game = get_object_or_404(Game, pk=game_uuid)
    #player = request.user.userprofile
    #team = player.game_team(game)

    #if not player.plays(game):
        #return Response(
            #{'error': _('The player does not participate in this game')},
            #status=status.HTTP_403_FORBIDDEN)
    #if data['code'] != game.start_keyword:
        #return Response(
            #{'error': _('Wrong start code')},
            #status=status.HTTP_403_FORBIDDEN)
    #longitude = data.get('lon')
    #latitude = data.get('lat')
    #if latitude is not None and longitude is not None:
        #team.store_position(player, latitude, longitude)
    #started_game = team.start_game()
    #if started_game.get('error'):
        #return Response(
            #serializers.ResponseStatusSerializer(started_game).data,
            #status=status.HTTP_400_BAD_REQUEST)
    #return Response(
        #serializers.ResponseStatusSerializer(started_game).data)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.GameFullDataSerializer},
    #operation_id='Game information',
    #description='GET player/games/{game_uuid}/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#@verified_session
#def game_full_data(request, game_uuid):
    #"""
    #full game information
    #"""
    #set_language(request.headers)
    #player = request.user.userprofile
    #game = get_object_or_404(Game, pk=game_uuid)
    #team = player.game_team(game)

    #if not player.plays(game):
        #return Response(
            #{'error': _('The player does not participate in this game')},
            #status=status.HTTP_403_FORBIDDEN)

    #if not (team.ready_to_play and not game.archived):
        #return Response(
            #{'error': _('The game is not ready to be downloaded')},
            #status=status.HTTP_403_FORBIDDEN)

    #serializer = serializers.GameFullDataSerializer(
        #{'game': team.game_detail_information(request)})

    #return Response(serializer.data.get('game'))


#@extend_schema(
    #methods=['post'],
    #request=serializers.VisitTaskSerializer,
    #responses={201: serializers.SuccessSerializer},
    #operation_id='Visit the game location',
    #description='POST player/task/{uuid}/visit/')
#@api_view(['POST'])
#@permission_classes([IsAuthenticated])
#@verified_session
#def visit_game_location(request, uuid):
    #"""
    #visit the game location by the team
    #"""
    #set_language(request.headers)
    #serializer = serializers.VisitTaskSerializer(data=request.data)
    #if not serializer.is_valid():
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #data = serializer.data
    #task = get_object_or_404(Task, pk=uuid)
    #game = task.game
    #player = request.user.userprofile
    #team = player.game_team(game)

    #if not player.plays(game):
        #return Response(
            #{'error': _('The player does not participate in this game')},
            #status=status.HTTP_403_FORBIDDEN)

    #if team.has_player(player.user) and team.started():
        #point = None
        #longitude = data.get('lon')
        #latitude = data.get('lat')
        #if latitude is not None and longitude is not None:
            #point = GeoPoint.objects.create(
                #latitude=latitude,
                #longitude=longitude)

        #dt = data.get('timestamp') or timezone.now()

        #completed_task = task.complete(
            #team, player, point, dt, completed=True)

        #return Response({'success': True}, status=status.HTTP_201_CREATED)
    #else:
        #return Response(
            #{'success': False}, status=status.HTTP_403_FORBIDDEN)


#@extend_schema(
    #methods=['post'],
    #request=serializers.CompleteTaskQuestSerializer,
    #responses={201: serializers.SuccessSerializer},
    #operation_id='Complete the quest task',
    #description='POST player/task/{uuid}/quest/')
#@api_view(['POST'])
#@permission_classes([IsAuthenticated])
#@verified_session
#def complete_quest(request, uuid):
    #"""
    #Complete the quest task by the team
    #"""
    #set_language(request.headers)
    #serializer = serializers.CompleteTaskQuestSerializer(data=request.data)
    #if not serializer.is_valid():
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #data = serializer.data
    #task = get_object_or_404(Task, uuid=uuid)
    #game = task.game
    #player = request.user.userprofile
    #team = player.game_team(game)
    #answers = data['answers']

    #if team.has_player(player.user) and team.started():
        #point = None
        #longitude = data.get('lon')
        #latitude = data.get('lat')
        #if latitude is not None and longitude is not None:
            #point = GeoPoint.objects.create(
                #latitude=latitude,
                #longitude=longitude)

        #completed_task = task.complete(
            #team,
            #player,
            #point,
            #dt=data.get('timestamp') or timezone.now(),
            #completed=not data['need_verification'])

        #answers = TaskAttemptQuestAnswers.objects.create(
            #taskattempt=completed_task,
            #answers=data['answers'])

        #team.played = True
        #team.save()

        #return Response({'success': True}, status=status.HTTP_201_CREATED)
    #else:
        #return Response(
            #{'success': False}, status=status.HTTP_403_FORBIDDEN)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.TaskAttemptsSerializer},
    #operation_id='Get all team attempts',
    #description='GET player/team/{team_id}/attempts/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def team_attempts(request, team_id):
    #"""
    #get all attempts for the team
    #"""
    #player = request.user.userprofile
    #team = get_team_or_404(Team, pk=team_id)
    #game = team.game

    #if team.has_player(player.user):
        #task_ids = TaskAttempt.objects.filter(
            #team=team, task__game=game).values_list('task', flat=True).distinct()
        #lst = [team_attempt_info(task.team_attempts(team), player, task)
               #for task in game.active_tasks().filter(uuid__in=task_ids)]
        #return Response(
            #serializers.TaskAttemptsSerializer({'tasks': lst}).data)
    #else:
        #return Response(
            #{'error': _('The player must be a member of this team')},
            #status=status.HTTP_403_FORBIDDEN)


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.AuthorGameSerializer},
    #operation_id='Author game information',
    #description='GET author/game/{game_uuid}/')
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def author_game(request, game_uuid):
    #"""
    #game information for author
    #"""
    #set_language(request.headers)
    #player = request.user.userprofile
    #game = get_object_or_404(Game, pk=game_uuid)

    #if not game.is_author(request.user):
        #return Response(
            #{'error': _('The user must be the author of this game')},
            #status=status.HTTP_403_FORBIDDEN)

    #serializer = serializers.AuthorGameSerializer(game)
    ## set '' for field if None

    #return Response(serializer.data)


#@extend_schema(
    #methods=['post'],
    #request=serializers.UpdateGameSerializer,
    #responses={201: serializers.StatusSerializer},
    #operation_id='Update the game fields',
    #description='POST author/update/game/{game_uuid}/')
#@api_view(['POST'])
#@permission_classes([IsAuthenticated])
#def game_update(request, game_uuid):
    #"""
    #update the game fields
    #"""
    #request_data = request.data
    #serializer = serializers.UpdateGameSerializer(data=request.data)

    #if not serializer.is_valid():
        #return Response(
            #error_response(serializer.errors),
            #status=status.HTTP_400_BAD_REQUEST)

    #data = serializer.data

    #game = get_object_or_404(Game, pk=game_uuid)
    #author = request.user.userprofile

    #if not game.is_author(author.user):
        #return Response(
            #{'error': _('The user must be the author of this game')},
            #status=status.HTTP_403_FORBIDDEN)

    #if 'name' in request_data:
        #game.name = data['name']
    #if 'short_name' in request_data:
        #game.short_name = data['short_name']
    #if 'description' in request_data:
        #game.description = data.get('description', '')
    #if 'short_description' in request_data:
        #game.short_description = data.get('short_description', '')
    #if 'startplace' in request_data:
        #game.startplace = data.get('startplace', '')
    #if 'regulations' in request_data:
        #if data['regulations']:
            #game.regulation = get_object_or_404(Regulation, slug=data['regulations'])
        #else:
            #game.regulation = None
    #if 'classifier' in request_data:
        #if data['classifier']:
            #game.classifier = get_object_or_404(Classifier, slug=data['classifier'])
        #else:
            #game.classifier = None
    #if 'transport' in request_data:
        #if data['transport']:
            #game.transport = get_object_or_404(Transport, slug=data['transport'])
        #else:
            #game.transport = None
    #if 'calculation_type' in request_data:
        #calculation_type = get_object_or_404(
            #GameCalculationType, slug=data['calculation_type'])
        #game.calculation_type = calculation_type
    #if 'max_players' in request_data:
        #game.max_players = data.get('max_players', '')
    #if 'min_players' in request_data:
        #game.min_players = data.get('min_players', '')
    #if 'max_teams' in request_data:
        #game.max_teams = data.get('max_teams', '')
    #if 'max_game_players' in request_data:
        #game.max_game_players = data.get('max_game_players', '')
    #if 'cost' in request_data:
        #game.cost = data.get('cost', '')
    #if 'start_keyword' in request_data:
        #game.start_keyword = data.get('start_keyword', '')
    #if 'language' in request_data:
        #game.language = data.get('language', '')
    #if 'abstract' in request_data:
        #game.abstract = data.get('abstract', '')
    #if 'published' in request_data:
        #game.published = data.get('published')
    #if 'archived' in request_data:
        #game.archived = data.get('archived')
    #if 'active' in request_data:
        #game.active = data.get('active')
    #if 'open' in request_data:
        #game.open = data.get('open')
    #if 'instant_results' in request_data:
        #game.instant_results = data.get('instant_results')
    #if 'public' in request_data:
        #game.public = data.get('public')
    #if 'use_offline_map' in request_data:
        #game.use_offline_map = data.get('use_offline_map')
    #if 'start' in request_data:
        #game.start = data.get('start')
    #if 'finish' in request_data:
        #game.finish = data.get('finish')
    #if 'deadline' in request_data:
        #game.deadline = data.get('deadline')

    #game.save()

    #return Response(
        #{'status': 'OK', 'uuid': game.uuid},
        #status=status.HTTP_201_CREATED)


#class GamePhotoUploadView(APIView):
    #"""
    #upload game photo
    #"""
    #permission_classes = [IsAuthenticated]
    #parser_class = (FileUploadParser, )

    #@extend_schema(
        #request=serializers.GamePhotoSerializer,
        #responses={201: serializers.StatusSerializer},
        #operation_id='Upload game photo',
        #description='POST author/upload/game/photo/')
    #def post(self, request, *args, **kwargs):
        #"""
        #overrided method
        #creates new photo or updates existent one
        #"""
        #game = get_object_or_404(
            #Game, pk=request.data.get('uuid'))

        #if not game.is_author(request.user):
            #return Response(
                #{'error': _('The user must be the author of this game')},
                #status=status.HTTP_403_FORBIDDEN)

        #serializer = serializers.GamePhotoSerializer(
            #game, data=request.data)

        #if serializer.is_valid():
            #serializer.save()
            #return Response({'status': 'OK'}, status=status.HTTP_201_CREATED)
        #else:
            #return Response(
                #error_response(serializer.errors),
                #status=status.HTTP_400_BAD_REQUEST)


#def set_language(headers):
    #"""
    #set language of translation in the view
    #"""
    #DEFAULT_LANGUAGE = 'en'
    #language = headers.get(HEADERS.LANGUAGE)
    #if not language in settings.LANGUAGE_CODES:
        #language = DEFAULT_LANGUAGE
    #translation.activate(language)


#def set_attempt_telemetry(photo, data):
    #"""
    #fill TaskAttemptPhoto.algorithm_telemetry from some dictionary
    #"""
    #algorithm_telemetry = data.get('algorithm_telemetry')
    #if algorithm_telemetry is not None:
        #algorithm_telemetry = json.loads(algorithm_telemetry)

        #photo.algorithm_telemetry = algorithm_telemetry
        #photo.save()


#def team_attempt_info(attempts, player, task):
    #"""
    #returns data structure for task attempts
    #"""
    #task.attempts_count = attempts.count()
    #task.mine_attempts = attempts.filter(player=player.user).count()
    #task.other_attempts = attempts.exclude(player=player.user).count()

    #task.attempts_auto_count = None
    #task.mine_auto_attempts = None
    #task.other_auto_attempts = None
    #if task.task_type.slug == 'algorithm':
        #task.attempts_auto_count = attempts.filter(
            #completed=True, reviewed=False).count()
        #task.mine_auto_attempts = attempts.filter(
            #player=player.user).filter(completed=True, reviewed=False).count()
        #task.other_auto_attempts = attempts.exclude(
            #player=player.user).filter(completed=True, reviewed=False).count()
    #return task


#@extend_schema(
    #methods=['get'],
    #responses={200: serializers.GameHintsSerializer},
    #operation_id="Game hints",
    #description='GET game/{game_uuid}/hints/{destination}')
#@api_view(['GET'])
#def game_hints(request, game_uuid, destination='web'):
    #"""
    #game hints
    #"""
    #set_language(request.headers)
    #game = get_object_or_404(Game, pk=game_uuid)
    #player = request.user.userprofile if request.user.is_authenticated else None
    #game_hints = game.get_hints(player, destination)
    #serializer = serializers.GameHintsSerializer({'hints': game_hints})
    #data = serializer.data

    #return Response(data)
