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
# from drf_spectacular.utils import extend_schema
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect, QueryDict, Http404
from django.contrib.auth import get_user_model
from django.utils import timezone, translation
from django.utils.translation import gettext_lazy as _

from routes.mountains.models import Ridge
#from fcuser.pipeline import get_unique_random_name, update_user_photo
from routes.api.models import App, AppVersion, UserAppVersion
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


@swagger_auto_schema(
    method='get',
    operation_description="GET hello/",
    responses={200: serializers.StatusSerializer})
@api_view(['GET'])
def hello_world(request):
    """
    test api method
    """
    data = {
        'status': 'OK',
        "message": "Hello, world!"
    }
    return Response(
        serializers.StatusSerializer(data).data)


class RidgeList(APIView):
    """
    List of ridges
    """
    @swagger_auto_schema(
        responses={200: serializers.RidgeOutSerializer(many=True)})
    def get(self, request):
        ridges = Ridge.objects.order_by('name')
        serializer = serializers.RidgeOutSerializer(
            ridges, many=True)
        return Response(serializer.data)


class RidgeNew(APIView):
    """
    Add a new ridge
    """
    @swagger_auto_schema(
        operation_description="POST ridges/new/",
        request_body=serializers.RidgeInSerializer,
        responses={201: serializers.RidgeOutSerializer})
    def post(self, request):
        serializer = serializers.RidgeInSerializer(
            data=request.data)
        if serializer.is_valid():
            ridge = serializer.save()
            serializer_out = serializers.RidgeOutSerializer(ridge)
            return Response(
                serializer_out.data,
                status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RidgeDetail(APIView):
    """
    Retrieve, update or delete a ridge instance
    """

    def get_object(self, slug):
        """
        get object
        """
        try:
            return Ridge.objects.get(slug=slug)
        except Ridge.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_description="GET ridge/{slug}/",
        responses={200: serializers.RidgeOutSerializer})
    def get(self, request, slug):
        """
        get ridge instance
        """
        ridge = self.get_object(slug)
        serializer = serializers.RidgeOutSerializer(ridge)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="PUT ridge/{slug}/",
        request_body=serializers.RidgeInSerializer,
        responses={200: serializers.RidgeOutSerializer})
    def put(self, request, slug):
        """
        update the ridge instance
        """
        ridge = self.get_object(slug)
        serializer = serializers.RidgeInSerializer(
            ridge, data=request.data)
        if serializer.is_valid():
            ridge = serializer.save()
            serializer_out = serializers.RidgeOutSerializer(ridge)
            return Response(serializer_out.data)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="DELETE ridge/{slug}/",
        responses={200: serializers.StatusSerializer})
    def delete(self, request, slug):
        ridge = self.get_object(slug)
        ridge.delete()
        data = {
            'status': 'OK',
            "message": f"Ridge {slug} is deleted"
        }
        return Response(
            serializers.StatusSerializer(data).data)


# class PhotoUploadView(APIView):
    # """
    # send task photo of the team
    # """
    #permission_classes = [IsAuthenticated]
    #parser_class = (FileUploadParser, )

    # @extend_schema(
        # request=serializers.CompleteTaskSerializer,
        #responses={201: serializers.SuccessSerializer},
        #operation_id='Upload team task photo',
        # description='POST player/task/{uuid}/photo/')
    # def post(self, request, uuid, *args, **kwargs):
        # """
        # overrided method
        # creates new photo or updates existent one
        # """
        #fmt = '%Y-%b-%d %H:%M:%S %Z %z'
        # set_language(request.headers)

        #task = get_object_or_404(Task, pk=uuid)
        #game = task.game
        #player = request.user.userprofile
        #team = player.game_team(game)

        #serializer = serializers.CompleteTaskSerializer(data=request.data)

        # if not serializer.is_valid():
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # if not player.verified_session(request.headers.get('X-Session-ID')):
        #raise Throttled(detail=_('Not valid session ID'))

        # if not team.has_player(request.user):
        # return Response({}, status=status.HTTP_403_FORBIDDEN)

        #post_data = serializer.data
        #point = None

        # if post_data.get('lat') and post_data.get('lon'):
        # point = GeoPoint.objects.create(
        # latitude=post_data['lat'],
        # longitude=post_data['lon'])

        #completed = not post_data['need_verification']
        #dt = post_data.get('timestamp') or timezone.now()

        # data = {
        # 'photo': request.data.get('image'),
        # 'team': team.id,
        # 'task': task.uuid
        # }

        #serializer = serializers.TaskAttemptPhotoSerializer(data=data)

        # if serializer.is_valid() and team.has_player(player.user) \
        # and team.started():
        #photo = serializer.save()

        # completed_task = task.complete(
        # team, player, point, dt, completed)

        #set_attempt_telemetry(photo, post_data)

        #photo.taskattempt = completed_task
        #photo.player = player.user

        #photo.found_points = post_data.get('found_points')
        # algorithm_parameters = post_data.get(
        # 'algorithm_parameters')
        # if algorithm_parameters is not None:
        #algorithm_parameters = json.loads(algorithm_parameters)
        #photo.algorithm_parameters = algorithm_parameters

        # algorithm_telemetry = post_data.get(
        # 'algorithm_telemetry')
        # if algorithm_telemetry is not None:
        #algorithm_telemetry = json.loads(algorithm_telemetry)
        #photo.algorithm_telemetry = algorithm_telemetry

        # photo.save()

        # return Response({'success': True}, status=status.HTTP_201_CREATED)
        # else:
        # return Response(
        # {'success': False}, status=status.HTTP_400_BAD_REQUEST)


# class LocationPhotoUploadView(APIView):
    # """
    # upload location photo
    # """
    #permission_classes = [IsAuthenticated]
    #parser_class = (FileUploadParser, )

    # @extend_schema(
        # request=serializers.LocationPhotoSerializer,
        #responses={201: serializers.StatusSerializer},
        #operation_id='Upload location photo',
        # description='POST author/upload/location/photo/')
    # def post(self, request, *args, **kwargs):
        # """
        # overrided method
        # creates new photo or updates existent one
        # """
        # location = get_object_or_404(
        # Location, pk=request.data.get('uuid'))

        # if not location.game.is_author(request.user):
        # return Response(
        #{'error': _('The user must be the author of this game')},
        # status=status.HTTP_403_FORBIDDEN)

        # serializer = serializers.LocationPhotoSerializer(
        # location, data=request.data)

        # if serializer.is_valid():
        # serializer.save()
        # return Response({'status': 'OK'}, status=status.HTTP_201_CREATED)
        # else:
        # return Response(
        # error_response(serializer.errors),
        # status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    methods=['post'],
    operation_description="POST jwt/logout/",
    request_body=serializers.TokenSerializer,
    responses={200: serializers.StatusSerializer})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_jwt_logout(request):
    """
    log out user
    """
    set_language(request.headers)

    user = request.user
    player = user.userprofile

    serializer = serializers.TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    refresh_token = serializer.data.get('refresh')
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        session = player.active_player_session()
        if session:
            session.delete = timezone.now()
            session.active = False
            session.save()
    except TokenError:
        return Response(
            {'error': 'Bad refresh token'},
            status=status.HTTP_400_BAD_REQUEST)

    return Response({'status': 'OK'}, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    """ Replace the serializer with your custom """
    serializer_class = serializers.CustomTokenObtainPairSerializer


# def valid_google_response(data):
    # """
    # validate key fields in response
    # """
    # try:
    #iss = data['iss']
    #aud = data['aud']
    #verified = data['email_verified']
    #exp = data['exp']

    # if "accounts.google.com" in iss:
    # if aud == settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY:
    # if verified == 'true':
    #exp_date = datetime.fromtimestamp(int(exp))
    # if datetime.now() < exp_date:
    # return True
    # except ValueError:
    # pass
    # except KeyError:
    # pass
    # return False


# def register_google_user(email, data, more_data):
    # """
    # register new user using google data
    # """
    #username = get_unique_random_name()
    #password = get_user_model().objects.make_random_password(length=20)
    # user = get_user_model().objects.create(
    # username=username,
    # password=password,
    # email=email)

    #profile = user.userprofile
    #profile.new = False
    #profile.google_id = data.get('sub')
    #profile.first_name = data.get('given_name')
    #profile.last_name = data.get('family_name')
    #profile.language = data.get('locale') or 'en'

    # if more_data.get('phone'):
    #phone = more_data.get('phone')
    #phone = ''.join(filter(lambda i: i.isdigit(), phone))
    #profile.phone = phone

    # if more_data.get('birthday'):
    # if len(more_data.get('birthday').split('/')):
    # profile.birthday = datetime.strptime(
    # more_data.get('birthday'), '%Y/%m/%d').date()

    # if more_data.get('gender'):
    #gender = more_data.get('gender')
    #profile.gender = 0 if gender == 'male' else 1

    # profile.save()

    #picture = data.get('picture')
    # if picture:
    #update_user_photo(profile, picture)

    # return user


# @extend_schema(
    # methods=['post'],
    #responses={200: serializers.TokenPairSerializer},
    # request=serializers.GoogleTokenSerializer,
    #operation_id='Token by google token',
    # description='POST jwt/token/google/')
# @api_view(['POST'])
# def jwt_by_google_token(request):
    # """
    # get token by google id_token
    # """
    #serializer = serializers.GoogleTokenSerializer(data=request.data)
    # if not serializer.is_valid():
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #req_data = serializer.data
    # response = requests.get(
    # 'https://oauth2.googleapis.com/tokeninfo?id_token={}'.format(
    # req_data['token']))
    #data = json.loads(response.content)
    #email = data.get('email')

    # if not email:
    # return Response(
    # {'error': 'no email'}, status=status.HTTP_404_NOT_FOUND)

    # if email and valid_google_response(data):
    #new_user = False
    #user = get_user_model().objects.filter(email=email).first()
    # if req_data.get('register'):
    # if user is None:
    #user = register_google_user(email, data, req_data)
    #new_user = True
    # if user:
    #refresh = RefreshToken.for_user(user)
    # serializer = serializers.TokenPairSerializer({
    # 'superuser': user.is_superuser,
    # 'refresh': str(refresh),
    # 'access': str(refresh.access_token),
    # 'jti': str(refresh.get('jti')),
    # })
    #response_status = status.HTTP_200_OK
    # if new_user:
    #response_status = status.HTTP_201_CREATED
    # return Response(serializer.data, status=response_status)
    # else:
    # return Response(
    # {'error': 'user not found'}, status=status.HTTP_401_UNAUTHORIZED)
    # return Response(
    # {'error': 'invalid id_token'}, status=status.HTTP_400_BAD_REQUEST)


# @extend_schema(
    # methods=['post'],
    #responses={200: serializers.PlayerSessionsSerializer},
    # request=serializers.UUIDSerializer,
    #operation_id='Player session',
    # description='POST player/auth/session/')
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def player_session(request):
    # """
    # create or update player session
    # """
    # set_language(request.headers)
    #player = request.user.userprofile

    #serializer = serializers.UUIDSerializer(data=request.data)

    # if not serializer.is_valid():
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #uuid = serializer.data.get('uuid')

    #other_sessions = player.other_sessions(uuid)
    # if not other_sessions:
    #session = player.get_or_create_session(uuid, request.headers)
    #serializer = serializers.UUIDSerializer({'uuid': session.id})
    # return Response(serializer.data, status=status.HTTP_201_CREATED)
    # else:
    # serializer = serializers.PlayerSessionsSerializer(
    # {'sessions': other_sessions})
    # return Response(serializer.data, status=status.HTTP_200_OK)


# @extend_schema(
    # methods=['post'],
    #responses={200: serializers.UUIDSerializer},
    # request=serializers.UUIDSerializer,
    #operation_id='Player force session',
    # description='POST player/auth/session/force/')
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def player_force_session(request):
    # """
    # force player session
    # """
    # set_language(request.headers)
    #player = request.user.userprofile

    #serializer = serializers.UUIDSerializer(data=request.data)

    # if not serializer.is_valid():
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #uuid = serializer.data.get('uuid')

    #session = player.get_or_create_session(uuid, request.headers)
    #other_sessions = player.other_sessions(uuid)
    # if other_sessions:
    # for session in other_sessions:
    #session.delete = timezone.now()
    #session.active = False
    # session.save()
    #serializer = serializers.UUIDSerializer({'uuid': session.id})
    # return Response(serializer.data, status=status.HTTP_201_CREATED)


def set_language(headers):
    """
    set language of translation in the view
    """
    DEFAULT_LANGUAGE = 'en'
    language = headers.get(HEADERS.LANGUAGE)
    if not language in settings.LANGUAGE_CODES:
        language = DEFAULT_LANGUAGE
    translation.activate(language)


