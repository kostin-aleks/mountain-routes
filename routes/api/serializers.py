"""
Serializers define the API representation.
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from routes.mountains.models import Ridge
#from location.models import Location
#from task.models import Task, TaskAttemptPhoto
#from team.models import Team

#DT_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
#DATE_FORMAT = "%Y-%m-%d"


# class GameSerializer(serializers.ModelSerializer):
# """
# Serializer for model Game
# """
# class Meta:
#model = Game
# fields = ('uuid', 'name', 'country_id', 'description', 'city_id',
#'photo', 'start', 'finish', 'deadline', 'published', 'archived',
#'calculation_type_id', 'single', 'min_players',
#'max_players', 'max_teams', 'cost', 'start_keyword', 'country_iso',
# 'transport', 'classifier', 'authors_list')
#depth = 1


# class AuthorSerializer(serializers.ModelSerializer):
# """
# Serializer for model User
# """
# class Meta:
#model = get_user_model()
#fields = ['id', 'username', 'first_name', 'last_name', 'email']


# class LocationSerializer(serializers.ModelSerializer):
# """
# Serializer for model Location
# """

# class Meta:
#model = Location
# fields = (
#'uuid', 'game', 'location_type',
#'name', 'short_name', 'description', 'start_minutes',
#'finish_minutes', 'photo', 'point', 'author'
# )
#depth = 1


# class PointSerializer(serializers.Serializer):  # TODO Method 'create' is abstract for all classes
# """
# Serializer for single point
# """
#longitude = serializers.FloatField()
#latitude = serializers.FloatField()


# class PlayerInfoSerializer(serializers.Serializer):
# """
# Serializer for Player short information
# """
#username = serializers.CharField()
#first_name = serializers.CharField(required=False)
#last_name = serializers.CharField(required=False)


# class LocationShortSerializer(serializers.Serializer):
# """
# Serializer for Location
# """
#uuid = serializers.UUIDField()
#name = serializers.CharField()
#game_id = serializers.CharField()


# class LocationInfoSerializer(serializers.Serializer):
# """
# Serializer for Location Info
# """
#uuid = serializers.UUIDField()
#short_name = serializers.CharField()
#name = serializers.CharField()
#number = serializers.IntegerField()
#tasks_count = serializers.IntegerField()


# class LocationAuthorSerializer(serializers.Serializer):
# """
# Serializer for Location Info, author api
# """
#uuid = serializers.UUIDField()
#short_name = serializers.CharField()
#number = serializers.IntegerField()
#tasks_count = serializers.IntegerField()
#base_score_sum = serializers.IntegerField()
#visible = serializers.BooleanField()
#finish = serializers.BooleanField()
#created = serializers.DateTimeField(format=DT_FORMAT)
#author = PlayerInfoSerializer()
#radius = serializers.IntegerField()
#description = serializers.CharField()
#point = PointSerializer()
#hint = serializers.CharField()
#photo = serializers.ImageField()


# class GameLocationsSerializer(serializers.Serializer):
# """
# Serializer for list of game locations
# """
#game_uuid = serializers.UUIDField()
# locations = serializers.ListField(
# child=LocationAuthorSerializer())


# class CitySerializer(serializers.Serializer):
# """
# Serializer for City
# """
#geoname_id = serializers.IntegerField()
#name = serializers.CharField()
#country_iso = serializers.CharField()


# class CityInfoSerializer(serializers.Serializer):
# """
# Serializer for City
# """
#name = serializers.CharField()
#geoname_id = serializers.CharField()


# class TaskSerializer(serializers.ModelSerializer):
# """
# Serializer for model Task
# """
# class Meta:
#model = Task
# fields = (
#'uuid', 'game', 'location', 'author_id', 'num',
#'photo', 'text', 'hint', 'answers', 'difficulty',
# )


# class TeamPlayerSerializer(serializers.ModelSerializer):
# """
# Serializer for model User
# """
# class Meta:
#model = get_user_model()
#fields = ['id', 'username', 'first_name', 'last_name', 'email']


# class TeamSerializer(serializers.ModelSerializer):
# """
# Serializer for model Team
# """
#players = TeamPlayerSerializer(many=True, read_only=True)

# class Meta:
#model = Team
# fields = (
#'id', 'game', 'creator_id', 'name', 'paid', 'number',
# 'place', 'score', 'accepted', 'created', 'players', )
#depth = 1


# TODO lets remove unused serializers like this one
# class GameTeamsSerializer(serializers.Serializer):
# """
# Serializer for list of game teams
# """
# teams = serializers.ListField(
# child=TeamSerializer())


# class TransportSerializer(serializers.ModelSerializer):
# """
# Serializer for model Transport
# """
# class Meta:
#model = Transport
# fields = (
# 'id', 'slug', 'name')


# class ClassifierSerializer(serializers.ModelSerializer):
# """
# Serializer for model Classifier
# """
# class Meta:
#model = Classifier
# fields = (
# 'id', 'slug', 'name', 'description', 'active')


# class ClassifierInfoSerializer(serializers.Serializer):
# """
# Serializer for model Classifier
# """
#slug = serializers.CharField()
#name = serializers.CharField()


# class TransportInfoSerializer(serializers.Serializer):
# """
# Serializer for model Transport
# """
#slug = serializers.CharField()
#name = serializers.CharField()


class UserOutSerializer(serializers.Serializer):
    """
    Serializer for User
    """
    username = serializers.CharField()
    id = serializers.IntegerField()


class RidgeOutSerializer(serializers.ModelSerializer):
    """
    Serializer for Ridge
    """
    class Meta:
        model = Ridge
        fields = '__all__'

    editor = UserOutSerializer()


class RidgeInSerializer(serializers.ModelSerializer):
    """
    Serializer for Ridge (In)
    """
    class Meta:
        model = Ridge
        fields = ['name', 'description']


# class CountryInfoSerializer(serializers.Serializer):
# """
# Serializer for Country
# """
#iso = serializers.CharField()
#name = serializers.CharField()


# class CountryShortInfoSerializer(serializers.Serializer):
# """
# Serializer for Country
# """
#iso = serializers.CharField()
#name = serializers.CharField()


# class RegulationSerializer(serializers.Serializer):

# """
# Serializer for Regulation
# """
#slug = serializers.CharField()
#name = serializers.CharField()
#short_name = serializers.CharField()
#description = serializers.CharField()
#text = serializers.CharField()
#active = serializers.BooleanField()


# class RegulationInfoSerializer(serializers.Serializer):
# """
# Serializer for Regulation
# """
#slug = serializers.CharField()
#text = serializers.CharField()


# class TotalScoreSerializer(serializers.Serializer):
# """
# Serializer for Player total score
# """
#score = serializers.IntegerField()
#place = serializers.IntegerField()


# class PodiumScoreSerializer(TotalScoreSerializer):
# """
# Serializer for score calculated as result related to podiums
# """
#score = serializers.IntegerField()
#place = serializers.IntegerField()
#podium_gold = serializers.IntegerField()
#podium_silver = serializers.IntegerField()
#podium_bronze = serializers.IntegerField()


# class PlayerRatingSerializer(serializers.Serializer):
# """
# Serializer for Player rating data
# """
#players_count = serializers.IntegerField()
#total_score = TotalScoreSerializer(required=False)
#year_score = TotalScoreSerializer(required=False)
#average_percent = TotalScoreSerializer(required=False)
#podium_score = PodiumScoreSerializer(required=False)


# class PlayerSerializer(serializers.Serializer):
# """
# Serializer for Player data
# """
#username = serializers.CharField()
#first_name = serializers.CharField()
#last_name = serializers.CharField()
#email = serializers.CharField()
#country = CountryInfoSerializer()
#city = CitySerializer()
#phone = serializers.CharField()
#phone_code = serializers.CharField()
#gender = serializers.IntegerField()
#language = serializers.CharField()
#photo = serializers.ImageField()
#player_rating = PlayerRatingSerializer()
#author_rating = serializers.IntegerField()
#date_joined = serializers.DateTimeField()
#birthday = serializers.DateField()
#is_active = serializers.BooleanField()


# class PlayersSerializer(serializers.Serializer):
# """
# Serializer for list of players
# """
# players = serializers.ListField(
# child=PlayerInfoSerializer())


# class AuthorsSerializer(serializers.Serializer):
# """
# Serializer for list of authors
# """
# authors = serializers.ListField(
# child=PlayerInfoSerializer())


# class PlayerShortInfoSerializer(serializers.Serializer):
# """
# Short info about Player
# """
#username = serializers.CharField()


# class GameShortInfoSerializer(serializers.Serializer):
# """
# Serializer for Game short information
# """
#uuid = serializers.UUIDField()
#short_name = serializers.CharField()
#transport = TransportSerializer(required=False)
#start = serializers.DateTimeField(format=DT_FORMAT)


# class GameShortSerializer(serializers.Serializer):
# """
# Serializer for Game short information
# """
#uuid = serializers.UUIDField()
#short_name = serializers.CharField()
#start = serializers.DateTimeField()


# class AuthorProfileSerializer(serializers.Serializer):
# """
# Serializer for Author Profile
# """
#username = serializers.CharField()
#first_name = serializers.CharField()
#last_name = serializers.CharField()
#email = serializers.CharField()
#country = CountryInfoSerializer()
#city = CitySerializer()
#phone = serializers.CharField()
#phone_code = serializers.CharField()
#gender = serializers.IntegerField()
#photo = serializers.ImageField()
#player_rating = PlayerRatingSerializer()
#author_rating = serializers.IntegerField()
#date_joined = serializers.DateTimeField()
#birthday = serializers.DateField()
#is_active = serializers.BooleanField()
# games = serializers.ListField(
# child=GameShortSerializer())


# class TeamInfoSerializer(serializers.Serializer):
# """
# Serializer for Team
# """
#uuid = serializers.UUIDField()
#name = serializers.CharField()
#number = serializers.IntegerField()
# players_list = serializers.ListField(
# child=PlayerShortInfoSerializer(), required=False)


# class TeamShortInfoSerializer(serializers.Serializer):
# """
# Serializer for Team short information
# """
#uuid = serializers.UUIDField()
#name = serializers.CharField()
#number = serializers.IntegerField()
#game = GameShortSerializer()


# class GameStatusSerializer(serializers.Serializer):
# """
# Serializer for Game Status
# """
#code = serializers.CharField()
#name = serializers.CharField()


# class AlgorithmParametersSerializer(serializers.Serializer):
# """
# Serializer for task's algorithm parameters
# """
#points = serializers.IntegerField(required=False)
#distance = serializers.IntegerField(required=False)
#max_image_size = serializers.IntegerField(required=False)


# class TimezoneSerializer(serializers.Serializer):
# """
# Serializer for time zone information
# """
#timezone = serializers.CharField()
#offset = serializers.CharField()


# class PlayerGameInfoSerializer(serializers.Serializer):
# """
# Serializer for Game
# """
#uuid = serializers.UUIDField()
#name = serializers.CharField()
#start_stamp = serializers.DateTimeField(format=DT_FORMAT)
#finish_stamp = serializers.DateTimeField(format=DT_FORMAT)
#size = serializers.FloatField()
#timezone = TimezoneSerializer()
#category = TransportSerializer()
# team = serializers.ListField(
# child=PlayerInfoSerializer())
#photo = serializers.ImageField()
#max_players = serializers.IntegerField()
#max_teams = serializers.IntegerField()
#start_point = PointSerializer()
#start_keyword = serializers.CharField()
#city = serializers.CharField()
#team_name = serializers.CharField()
#team_id = serializers.IntegerField()
#team_game_number = serializers.CharField()
#team_game_class = serializers.CharField()
#status = serializers.CharField()
#language = serializers.CharField()
#abstract = serializers.CharField()
#use_offline_map = serializers.BooleanField()
#game_file_version = serializers.IntegerField()
#game_file_url = serializers.CharField()
#game_file_hash = serializers.CharField()
#game_file_size = serializers.IntegerField()


# class PlayerGamesSerializer(serializers.Serializer):
# """
# Serializer for Player games
# """
# result = serializers.ListField(
# child=PlayerGameInfoSerializer())


# class AuthorGameInfoSerializer(serializers.Serializer):
# """
# Serializer for Game
# """
#uuid = serializers.UUIDField()
#status = GameStatusSerializer()
#short_name = serializers.CharField()
# categories = serializers.ListField(
# child=TransportSerializer(), required=False)
#start = serializers.DateTimeField(format=DT_FORMAT)
#finish = serializers.DateTimeField(format=DT_FORMAT)
#cost = serializers.FloatField()
#description = serializers.CharField()
#start_keyword = serializers.CharField()
#finish_keyword = serializers.CharField()
#country = CountryInfoSerializer()
#photo = serializers.ImageField()
#city = CitySerializer()
#regulations = RegulationSerializer(source='regulation')
#open = serializers.BooleanField()
#tasks_count = serializers.IntegerField()
#locations_count = serializers.IntegerField()
#player_count = serializers.IntegerField()
#language = serializers.CharField()
#abstract = serializers.CharField()
#author_tasks = serializers.IntegerField()
#author_status = serializers.CharField()
# authors = serializers.ListField(
# child=PlayerInfoSerializer())


# class AuthorGamesSerializer(serializers.Serializer):
# """
# Serializer for Author games
# """
#author_id = serializers.IntegerField()
# games = serializers.ListField(
# child=AuthorGameInfoSerializer())


# class TaskAttemptSerializer(serializers.Serializer):
# """
# Serializer for Completed Task
# """
#task_uuid = serializers.UUIDField()
#task_num = serializers.CharField()
#location_uuid = serializers.UUIDField()
#score = serializers.IntegerField(required=False)


# class TaskShortSerializer(serializers.Serializer):
# """
# Serializer for Task. Short information
# """
#location_id = serializers.CharField()
#num = serializers.IntegerField()
#photo = serializers.ImageField()
#text = serializers.CharField()
#difficulty = serializers.IntegerField()


# class ParticipationSerializer(serializers.Serializer):
# """
# Serializer for Participation
# """
#code = serializers.IntegerField()
#status = serializers.CharField()


# class GameInfoSerializer(serializers.Serializer):
# """
# Serializer for Game
# """
#short_name = serializers.CharField()
#country = CountryInfoSerializer()
#city = CitySerializer()
#participation = ParticipationSerializer()
#start = serializers.DateField()


# class GamesSerializer(serializers.Serializer):
# """
# Serializer for Games
# """
# games = serializers.ListField(
# child=GameInfoSerializer())


# class GameDetailedSerializer(serializers.Serializer):
# """
# Serializer for detailed information about the game
# for the player
# """
#game = GameSerializer()
#player = serializers.IntegerField()
#participation = ParticipationSerializer()
#country = serializers.CharField()
#city = serializers.CharField()


# class LocationShortInfoSerializer(serializers.Serializer):
# """
# Serializer for detailed information about the game
# for the player
# """
#uuid = serializers.UUIDField()
#name = serializers.CharField()


class StatusSerializer(serializers.Serializer):
    """
    Serializer for response status message
    """
    status = serializers.CharField()
    message = serializers.CharField(required=False)
    id = serializers.IntegerField(required=False)


# class LocationTypeSerializer(serializers.Serializer):
    # """
    # Serializer for Location Type
    # """
    # id = serializers.IntegerField(required=False)  # pylint: disable=invalid-name
    #description = serializers.CharField()
    #slug = serializers.CharField()


# class LocationTypeInfoSerializer(serializers.Serializer):
    # """
    # Serializer for Location Type
    # """
    # id = serializers.IntegerField(required=False)  # pylint: disable=invalid-name
    #name = serializers.CharField()
    #slug = serializers.CharField()


# class TaskTypeSerializer(serializers.Serializer):
    # """
    # Serializer for Task Type
    # """
    # id = serializers.IntegerField()  # pylint: disable=invalid-name
    #description = serializers.CharField()
    #slug = serializers.CharField()


# class CalculationTypeSerializer(serializers.Serializer):
    # """
    # Serializer for Game Calculation Type
    # """
    #slug = serializers.CharField()


# class CalculationTypeInfoSerializer(serializers.Serializer):
    # """
    # Serializer for Game Calculation Type
    # """
    #slug = serializers.CharField()
    #name = serializers.CharField()


# class AlgorithmSerializer(serializers.Serializer):
    # """
    # Serializer for Task Algorithm
    # """
    #slug = serializers.CharField()
    #points = serializers.IntegerField()
    #distance = serializers.IntegerField()
    #min_k_soap = serializers.IntegerField()


# class TaskOptionsSerializer(serializers.Serializer):
    # """
    # Serializer for Task Algorithm
    # """
    #algorithm = AlgorithmSerializer(required=False)


# class TaskDataSerializer(serializers.Serializer):
    # """
    # Serializer for Task full information
    # """
    #uuid = serializers.UUIDField()
    #task_type = TaskTypeSerializer()
    #num = serializers.IntegerField()
    #photo = serializers.ImageField()
    #text = serializers.CharField()
    #hint = serializers.CharField()
    #answers = serializers.CharField()
    #point = PointSerializer()
    #base_score = serializers.IntegerField()
    #difficulty = serializers.IntegerField()
    #algorithm_points = serializers.IntegerField()
    #algorithm_distance = serializers.IntegerField()
    #location = LocationShortSerializer()
    #author = PlayerInfoSerializer()
    #control_point = serializers.BooleanField()
    #doable = serializers.CharField()
    #enterable = serializers.CharField()
    #visible = serializers.CharField()
    #radius = serializers.IntegerField()
    #created = serializers.DateTimeField(format=DT_FORMAT)
    #active = serializers.BooleanField()
    #options = TaskOptionsSerializer(required=False)


# class LocationDataSerializer(serializers.Serializer):
    # """
    # Serializer for Location full information
    # """
    #uuid = serializers.UUIDField()
    #location_type = LocationTypeInfoSerializer()
    #name = serializers.CharField()
    #short_name = serializers.CharField()
    #number = serializers.IntegerField()
    #description = serializers.CharField()
    #hint = serializers.CharField()
    #start_minutes = serializers.IntegerField()
    #finish_minutes = serializers.IntegerField()
    #photo = serializers.ImageField()
    #point = PointSerializer()
    #radius = serializers.IntegerField()
    #visible = serializers.BooleanField()
    #finish = serializers.BooleanField()
    #visitable = serializers.BooleanField()
    #task_list = TaskDataSerializer(read_only=True, many=True)


# class GameDataSerializer(serializers.Serializer):
    # """
    # Serializer for Game full information
    # """
    #uuid = serializers.UUIDField()
    #name = serializers.CharField()
    #short_name = serializers.CharField()
    #description = serializers.CharField()
    #category = TransportSerializer()
    #photo = serializers.ImageField()
    #size = serializers.FloatField()
    #status = serializers.CharField()
    #regulations = RegulationSerializer(source='regulation')
    #start_stamp = serializers.DateTimeField(format=DT_FORMAT)
    #finish_stamp = serializers.DateTimeField(format=DT_FORMAT)
    #start_point = PointSerializer()
    #finish_point = PointSerializer()
    #start_keyword = serializers.CharField()
    #city = serializers.CharField()
    # team = serializers.ListField(
    # child=PlayerInfoSerializer())
    #team_name = serializers.CharField()
    #team_id = serializers.IntegerField()
    #team_game_number = serializers.CharField()
    #team_game_class = serializers.CharField()
    #max_players = serializers.IntegerField()
    #max_teams = serializers.IntegerField()
    #timezone = TimezoneSerializer()
    #language = serializers.CharField()
    #abstract = serializers.CharField()
    #use_offline_map = serializers.BooleanField()
    # locations = LocationDataSerializer(
    # read_only=True, many=True, required=False)


# class GameFullDataSerializer(serializers.Serializer):
    # """
    # Serializer for detailed information about the game
    # for the player
    # """
    #game = GameDataSerializer()


# class AuthorGameSerializer(serializers.Serializer):
    # """
    # Serializer for Game for author
    # """
    #uuid = serializers.UUIDField()
    #name = serializers.CharField()
    #short_name = serializers.CharField()
    #description = serializers.CharField()
    #short_description = serializers.CharField()
    #startplace = serializers.CharField()
    #transport = TransportInfoSerializer()
    #photo = serializers.ImageField()
    #city = CityInfoSerializer()
    #country = CountryShortInfoSerializer()
    #published = serializers.BooleanField()
    #archived = serializers.BooleanField()
    #regulations = RegulationInfoSerializer(source='regulation')
    #classifier = ClassifierInfoSerializer()
    #created = serializers.DateTimeField(format=DT_FORMAT)
    #start = serializers.DateTimeField(format=DT_FORMAT)
    #finish = serializers.DateTimeField(format=DT_FORMAT)
    #deadline = serializers.DateTimeField(format=DT_FORMAT)
    #active = serializers.BooleanField()
    #open = serializers.BooleanField()
    #instant_results = serializers.BooleanField()
    #calculation_type = CalculationTypeInfoSerializer()
    #max_players = serializers.IntegerField()
    #min_players = serializers.IntegerField()
    #max_teams = serializers.IntegerField()
    #max_game_players = serializers.IntegerField()
    #public = serializers.BooleanField()
    #cost = serializers.IntegerField()
    #start_keyword = serializers.CharField()
    #language = serializers.CharField()
    #abstract = serializers.CharField()
    #use_offline_map = serializers.BooleanField()
    #photo_size = serializers.IntegerField()
    #registered_teams_count = serializers.IntegerField()
    #players_count = serializers.IntegerField()


# class ExportTaskSerializer(serializers.Serializer):
    # """
    # Serializer for Task export information
    # """
    #task_type = TaskTypeSerializer()
    #num = serializers.IntegerField()
    #photo = serializers.CharField()
    #photo_base64 = serializers.CharField()
    #text = serializers.CharField()
    #hint = serializers.CharField()
    #answers = serializers.CharField()
    #point = PointSerializer()
    #base_score = serializers.IntegerField()
    #difficulty = serializers.IntegerField()
    #algorithm_points = serializers.IntegerField()
    #algorithm_distance = serializers.IntegerField()
    #location = LocationShortSerializer()
    #author = PlayerInfoSerializer()
    #control_point = serializers.BooleanField()
    #doable = serializers.CharField()
    #enterable = serializers.CharField()
    #visible = serializers.CharField()
    #radius = serializers.IntegerField()


# class ExportLocationSerializer(serializers.Serializer):
    # """
    # Serializer for Location export information
    # """
    #location_type = LocationTypeInfoSerializer()
    #name = serializers.CharField()
    #short_name = serializers.CharField()
    #number = serializers.IntegerField()
    #description = serializers.CharField()
    #hint = serializers.CharField()
    #photo = serializers.CharField()
    #photo_base64 = serializers.CharField()
    #point = PointSerializer()
    #radius = serializers.IntegerField()
    #visible = serializers.BooleanField()
    #finish = serializers.BooleanField()
    #visitable = serializers.BooleanField()
    #author = PlayerInfoSerializer()
    #tasks = ExportTaskSerializer(read_only=True, many=True)


# class ExportGameDataSerializer(serializers.Serializer):
    # """
    # Serializer for Game export information
    # """
    #name = serializers.CharField()
    #short_name = serializers.CharField()
    #description = serializers.CharField()
    #transport = TransportSerializer()
    #classifier = ClassifierSerializer()
    #photo = serializers.CharField()
    #photo_base64 = serializers.CharField()
    #regulation = RegulationSerializer()
    #country = CountryInfoSerializer()
    #city = CitySerializer()
    #calculation_type = CalculationTypeSerializer()
    #min_players = serializers.IntegerField()
    #max_players = serializers.IntegerField()
    #max_teams = serializers.IntegerField()
    #start_point = PointSerializer()
    #finish_point = PointSerializer()
    #start_keyword = serializers.CharField()
    #top_left = PointSerializer()
    #bottom_right = PointSerializer()
    #language = serializers.CharField()
    #abstract = serializers.CharField()


# class ExportGameSerializer(serializers.Serializer):
    # """
    # Serializer for detailed information about the game
    # for export as json data
    # """
    #game = ExportGameDataSerializer()
    # locations = ExportLocationSerializer(
    # read_only=True, many=True, required=False)


# class PlayerTeamsSerializer(serializers.Serializer):
    # """
    # Serializer for Player teams
    # """
    #player_id = serializers.IntegerField()
    # teams_list = serializers.ListField(
    # child=TeamInfoSerializer())


# class LocationTaskListSerializer(serializers.Serializer):
    # """
    # Serializer for Location tasks
    # """
    #game_uuid = serializers.UUIDField()
    #location_uuid = serializers.UUIDField()
    # tasks_list = serializers.ListField(
    # child=TaskSerializer())


# class CompletedTaskSerializer(serializers.Serializer):
    # """
    # Serializer for the task with result
    # """
    #task = TaskShortSerializer()
    #team_id = serializers.IntegerField()
    #completed = serializers.BooleanField()


# class CompletedLocationSerializer(serializers.Serializer):
    # """
    # Serializer for list of game locations
    # """
    #location = LocationShortSerializer()
    # tasks = serializers.ListField(
    # child=CompletedTaskSerializer())


# class CompleteTaskQuestSerializer(serializers.Serializer):
    # """
    # Serializer for data to store completion of game task
    # of type quest by the team
    # """
    #need_verification = serializers.BooleanField()
    #timestamp = serializers.DateTimeField()
    #answers = serializers.CharField()
    #lon = serializers.FloatField(required=False)
    #lat = serializers.FloatField(required=False)


# class TeamStatisticsSerializer(serializers.Serializer):
    # """
    # Serializer for team game statistics
    # """
    #team = TeamShortInfoSerializer()
    #game = GameShortSerializer()
    #country = CountryInfoSerializer()
    #city = CitySerializer()
    #place = serializers.IntegerField()
    #game_class = serializers.CharField()
    #completed_tasks = serializers.IntegerField()
    #tasks_count = serializers.IntegerField()
    #locations_count = serializers.IntegerField()
    # locations = serializers.ListField(
    # child=CompletedLocationSerializer())


# class CoordinatesSerializer(serializers.Serializer):
    # """
    # Serializer for coordinates
    # """
    #longitude = serializers.FloatField()
    #latitude = serializers.FloatField()
    #good_gps = serializers.BooleanField(required=False)
    #game_uuid = serializers.UUIDField(required=False)
    #team_id = serializers.IntegerField(required=False)


# class CouplePointsSerializer(serializers.Serializer):
    # """
    # Serializer for couple of points
    # """
    #longitude1 = serializers.FloatField()
    #latitude1 = serializers.FloatField()
    #longitude2 = serializers.FloatField()
    #latitude2 = serializers.FloatField()


# class VisitLocationSerializer(serializers.Serializer):
    # """
    # Serializer for data to store visiting the location by the team
    # """
    #location_uuid = serializers.UUIDField()
    #team_id = serializers.IntegerField()


# class NearestLocationSerializer(serializers.Serializer):
    # """
    # Serializer for nearest location
    # """
    #team = TeamShortInfoSerializer()
    #location = LocationShortSerializer()
    #distance = serializers.IntegerField()
    #inside = serializers.BooleanField()


# class CompleteTaskSerializer(serializers.Serializer):
    # """
    # Serializer for data to store completion of game task by the team
    # """
    #need_verification = serializers.BooleanField()
    #timestamp = serializers.DateTimeField(required=False)
    #lon = serializers.FloatField(required=False)
    #lat = serializers.FloatField(required=False)
    #algorithm_parameters = serializers.CharField(required=False)
    #algorithm_telemetry = serializers.CharField(required=False)
    #found_points = serializers.IntegerField(required=False)


# class TaskAttemptPhotoSerializer(serializers.ModelSerializer):
    # """
    # Serializer for data to store the photo of game task by the team
    # """
    # class Meta:
    #model = TaskAttemptPhoto
    #fields = ['task', 'team', 'photo']


# class PhotoUploadSerializer(serializers.ModelSerializer):
    # """
    # Serializer for data to store the photo of game task by the team
    # """
    # class Meta:
    #model = TaskAttemptPhoto
    #fields = ['photo']


# class LanguageSerializer(serializers.Serializer):
    # """
    # Serializer for languages
    # """
    #code = serializers.CharField()
    #name = serializers.CharField()


# class LanguagesSerializer(serializers.Serializer):
    # """
    # Serializer for languages
    # """
    # languages = serializers.ListField(
    # child=LanguageSerializer())


# class TeamCompletedTaskSerializer(serializers.Serializer):
    # """
    # Serializer for completion of the game task by the team
    # """
    #task = TaskShortSerializer()
    #team_id = serializers.IntegerField()
    #completed = serializers.BooleanField()


# class GameLocationSerializer(serializers.Serializer):
    # """
    # Serializer for Location with team results
    # """
    #location = LocationSerializer()
    # tasks = serializers.ListField(
    # child=TeamCompletedTaskSerializer())


# class TeamTaskAttemptsSerializer(serializers.Serializer):
    # """
    # Serializer for information about Task attempts for single team
    # """
    #uuid = serializers.UUIDField()
    #task_type = TaskTypeSerializer()
    #num = serializers.IntegerField()
    #photo = serializers.ImageField()
    #text = serializers.CharField()
    #hint = serializers.CharField()
    #answers = serializers.CharField()
    #point = PointSerializer()
    #base_score = serializers.IntegerField()
    #difficulty = serializers.IntegerField()
    #algorithm_points = serializers.IntegerField()
    #algorithm_distance = serializers.IntegerField()
    #location = LocationShortSerializer()
    #author = PlayerInfoSerializer()
    #control_point = serializers.BooleanField()
    #doable = serializers.CharField()
    #enterable = serializers.CharField()
    #visible = serializers.CharField()
    #radius = serializers.IntegerField()
    #attempts_count = serializers.IntegerField()
    #mine_attempts = serializers.IntegerField()
    #other_attempts = serializers.IntegerField()
    #attempts_auto_count = serializers.IntegerField()
    #mine_auto_attempts = serializers.IntegerField()
    #other_auto_attempts = serializers.IntegerField()


# class TaskAttemptsSerializer(serializers.Serializer):
    # """
    # Serializer for team attempts for the game tasks
    # """
    # tasks = serializers.ListField(
    # child=TeamTaskAttemptsSerializer())


# class TeamGameLocationsSerializer(serializers.Serializer):
    # """
    # Serializer for game locations with team results
    # """
    #game = serializers.CharField()
    #team = serializers.IntegerField()
    # locations = serializers.ListField(
    # child=GameLocationSerializer())


# class LocationTasksSerializer(serializers.Serializer):
    # """
    # Serializer for game location with its tasks
    # """
    #location = LocationSerializer()
    # tasks = serializers.ListField(
    # child=TaskSerializer())


# class GameTasksSerializer(serializers.Serializer):
    # """
    # Serializer for all game locations with tasks
    # """
    # locations = serializers.ListField(
    # child=LocationTasksSerializer())


# class KeywordSerializer(serializers.Serializer):
    # """
    # Serializer for game keyword
    # """
    #keyword = serializers.CharField()


# class KeywordAndPositionSerializer(serializers.Serializer):
    # """
    # Serializer for game keyword and user position
    # """
    #code = serializers.CharField()
    #lat = serializers.FloatField(required=False)
    #lon = serializers.FloatField(required=False)


# class GamePaymentSerializer(serializers.Serializer):
    # """
    # Serializer for team's payment for game
    # """
    #game = GameShortInfoSerializer()
    #team = TeamInfoSerializer()
    #user = PlayerInfoSerializer()
    #amount = serializers.FloatField()
    #added = serializers.DateTimeField()


# class PaymentSerializer(serializers.Serializer):
    # """
    # Serializer for team's payment for game
    # """
    #game_uuid = serializers.UUIDField()
    #team_id = serializers.IntegerField()
    #player_id = serializers.IntegerField()
    #amount = serializers.FloatField()


# class GamePaymentsSerializer(serializers.Serializer):
    # """
    # Serializer for team's payments for game
    # """
    # payments = serializers.ListField(
    # child=GamePaymentSerializer())


# class PlayerProfileSerializer(serializers.Serializer):
    # """
    # Serializer for player profile
    # """
    #username = serializers.CharField()
    #first_name = serializers.CharField()
    #last_name = serializers.CharField()
    #photo = serializers.ImageField()
    #email = serializers.CharField()
    #country = CountryInfoSerializer()
    #city = CitySerializer()
    #phone = serializers.CharField()
    #phone_code = serializers.CharField()
    #gender = serializers.IntegerField()
    #language = serializers.CharField(required=False)
    #player_rating = PlayerRatingSerializer()
    #author_rating = serializers.IntegerField()
    #date_joined = serializers.DateTimeField(format=DATE_FORMAT, required=False)
    #birthday = serializers.DateField(format=DATE_FORMAT, required=False)
    #is_active = serializers.BooleanField(required=False)


# class ResponseStatusSerializer(serializers.Serializer):
    # """
    # Serializer for response status message
    # """
    #success = serializers.CharField(required=False)
    #error = serializers.CharField(required=False)
    # id = serializers.IntegerField(required=False)  # pylint: disable=invalid-name
    #uuid = serializers.UUIDField(required=False)


# class DistanceSerializer(serializers.Serializer):
    # """
    # Serializer for distance
    # """
    #distance = serializers.CharField()
    #unit = serializers.CharField()


# class IDSerializer(serializers.Serializer):
    # """
    # Serializer for response with id of created object
    # """
    # id = serializers.IntegerField()  # pylint: disable=invalid-name


# class UUIDSerializer(serializers.Serializer):
    # """
    # Serializer for response with uuid of created object
    # """
    #uuid = serializers.UUIDField()


# class GameItemsCountSerializer(serializers.Serializer):
    # """
    # Serializer for counts of game items
    # """
    #game = GameShortInfoSerializer()
    #locations_count = serializers.IntegerField()
    #tasks_count = serializers.IntegerField()


# class AddLocationSerializer(serializers.Serializer):
    # """
    # Serializer for Location fields to add new location
    # """
    #game_uuid = serializers.UUIDField(required=False)
    #uuid = serializers.UUIDField(required=False)
    #name = serializers.CharField()
    #short_name = serializers.CharField()
    #description = serializers.CharField(required=False, allow_blank=True)
    #hint = serializers.CharField(required=False, allow_blank=True)
    #number = serializers.IntegerField(required=False)
    #location_type = serializers.CharField()
    #start_minutes = serializers.IntegerField(required=False)
    #finish_minutes = serializers.IntegerField(required=False)
    #latitude = serializers.FloatField(required=False)
    #longitude = serializers.FloatField(required=False)
    #radius = serializers.IntegerField(required=False)
    #visible = serializers.BooleanField(required=False)
    #finish = serializers.BooleanField(required=False)
    #active = serializers.BooleanField(required=False)


# class UpdateLocationSerializer(serializers.Serializer):
    # """
    # Serializer for Location fields to update the location
    # """
    #name = serializers.CharField(required=False)
    #short_name = serializers.CharField(required=False)
    #description = serializers.CharField(required=False, allow_blank=True)
    #hint = serializers.CharField(required=False, allow_blank=True)
    #number = serializers.IntegerField(required=False)
    #location_type = serializers.CharField(required=False)
    #start_minutes = serializers.IntegerField(required=False)
    #finish_minutes = serializers.IntegerField(required=False)
    #latitude = serializers.FloatField(required=False)
    #longitude = serializers.FloatField(required=False)
    #radius = serializers.IntegerField(required=False)
    #visible = serializers.BooleanField(required=False)
    #finish = serializers.BooleanField(required=False)
    #active = serializers.BooleanField(required=False)


# class UpdateGameSerializer(serializers.Serializer):
    # """
    # Serializer for Game fields to update the game
    # """
    #name = serializers.CharField(required=False)
    #short_name = serializers.CharField(required=False)
    #description = serializers.CharField(required=False, allow_blank=True)
    #short_description = serializers.CharField(required=False, allow_blank=True)
    #startplace = serializers.CharField(required=False, allow_blank=True)
    #published = serializers.BooleanField(required=False)
    #archived = serializers.BooleanField(required=False)
    #regulations = serializers.SlugField(required=False, allow_blank=True, source='regulation')
    #classifier = serializers.SlugField(required=False, allow_blank=True)
    #transport = serializers.SlugField(required=False, allow_blank=True)
    #active = serializers.BooleanField(required=False)
    #open = serializers.BooleanField(required=False)
    #instant_results = serializers.BooleanField(required=False)
    #calculation_type = serializers.SlugField(required=False)
    #max_players = serializers.IntegerField(required=False)
    #min_players = serializers.IntegerField(required=False)
    #max_teams = serializers.IntegerField(required=False)
    #max_game_players = serializers.IntegerField(required=False)
    #public = serializers.BooleanField(required=False)
    #cost = serializers.IntegerField(required=False)
    #start_keyword = serializers.CharField(required=False, allow_blank=True)
    #language = serializers.CharField(required=False, allow_blank=True)
    #abstract = serializers.CharField(required=False, allow_blank=True)
    #use_offline_map = serializers.BooleanField(required=False)
    #start = serializers.DateTimeField(required=False)
    #finish = serializers.DateTimeField(required=False)
    #deadline = serializers.DateTimeField(required=False)


# class LocationTypesSerializer(serializers.Serializer):
    # """
    # Serializer for list of location types
    # """
    # types = serializers.ListField(
    # child=LocationTypeSerializer())


# class UpdateTaskSerializer(serializers.Serializer):
    # """
    # Serializer for Task fields to update game task
    # """
    #task_type = serializers.CharField(required=False)
    #num = serializers.IntegerField(required=False)
    #text = serializers.CharField(allow_null=True, required=False)
    # hint = serializers.CharField(
    # allow_blank=True, allow_null=True, required=False)
    #answers = serializers.CharField(allow_null=True, required=False)
    #base_score = serializers.IntegerField(required=False)
    #difficulty = serializers.IntegerField(required=False)
    #latitude = serializers.FloatField(required=False)
    #longitude = serializers.FloatField(required=False)
    #algorithm_points = serializers.IntegerField(required=False)
    #algorithm_distance = serializers.IntegerField(required=False)
    #doable = serializers.CharField(required=False)
    #enterable = serializers.CharField(required=False)
    #visible = serializers.CharField(required=False)
    #radius = serializers.IntegerField(required=False)
    #active = serializers.BooleanField(required=False)


# class AddTaskSerializer(serializers.Serializer):
    # """
    # Serializer for Task fields to add new game task
    # """
    #uuid = serializers.UUIDField(required=False)
    #task_type = serializers.CharField()
    #num = serializers.IntegerField()
    #text = serializers.CharField(required=False)
    #hint = serializers.CharField(required=False, allow_blank=True)
    #answers = serializers.CharField(required=False)
    #base_score = serializers.IntegerField(required=False)
    #difficulty = serializers.IntegerField(required=False)
    #latitude = serializers.FloatField(required=False)
    #longitude = serializers.FloatField(required=False)
    #algorithm_points = serializers.IntegerField(required=False)
    #algorithm_distance = serializers.IntegerField(required=False)
    #doable = serializers.CharField(required=False)
    #enterable = serializers.CharField(required=False)
    #visible = serializers.CharField(required=False)
    #radius = serializers.IntegerField(required=False)
    #active = serializers.BooleanField(required=False)


# class AppVersionSerializer(serializers.Serializer):
    # """
    # Serializer for AppVersion fields
    # """
    #slug = serializers.CharField()
    #application = serializers.CharField()
    #version = serializers.CharField()
    #author = serializers.CharField()
    #created = serializers.DateTimeField(format=DATE_FORMAT)


# class TaskTypesSerializer(serializers.Serializer):
    # """
    # Serializer for list of task types
    # """
    # types = serializers.ListField(
    # child=TaskTypeSerializer())


# class TaskPhotoSerializer(serializers.ModelSerializer):
    # """
    # Serializer for data to store the photo of task by the author
    # """
    # class Meta:
    #model = Task
    #fields = ['uuid', 'photo']


# class LocationPhotoSerializer(serializers.ModelSerializer):
    # """
    # Serializer for data to store the photo of location by the author
    # """
    # class Meta:
    #model = Location
    #fields = ['uuid', 'photo']


# class GamePhotoSerializer(serializers.ModelSerializer):
    # """
    # Serializer for data to store the game image by the author
    # """
    # class Meta:
    #model = Game
    #fields = ['uuid', 'photo']


# class LoggedInPlayerSerializer(serializers.Serializer):
    # """
    # Serializer for logged in Player data
    # """
    #username = serializers.CharField()
    #first_name = serializers.CharField()
    #last_name = serializers.CharField()


# class PlayerSessionSerializer(serializers.Serializer):
    # """
    # Serializer for player session
    # """
    #user = LoggedInPlayerSerializer()
    #device = serializers.CharField()
    # os = serializers.CharField()    # pylint: disable=invalid-name
    #app_version = serializers.CharField()
    #active = serializers.BooleanField()
    #logged = serializers.DateTimeField()


# class PlayerSessionsSerializer(serializers.Serializer):
    # """
    # Serializer for list of sessions
    # """
    # sessions = serializers.ListField(
    # child=PlayerSessionSerializer())


# class AuthUserSerializer(serializers.Serializer):
    # """
    # Serializer for auth data of user
    # """
    #username = serializers.CharField()
    #password = serializers.CharField()


# class SuccessSerializer(serializers.Serializer):
    # """
    # Serializer for response success message
    # """
    #success = serializers.BooleanField()


# class VisitTaskSerializer(serializers.Serializer):
    # """
    # Serializer for visiting location data
    # """
    #timestamp = serializers.DateTimeField(required=False)
    #lon = serializers.FloatField(required=False)
    #lat = serializers.FloatField(required=False)


# class TokenSerializer(serializers.Serializer):
    # """
    # Serializer for token
    # """
    #refresh = serializers.CharField()


# class GoogleTokenSerializer(serializers.Serializer):
    # """
    # Serializer for google token
    # """
    #token = serializers.CharField()
    #register = serializers.BooleanField(required=False)
    #phone = serializers.CharField(required=False)
    #birthday = serializers.CharField(required=False)
    # gender = serializers.ChoiceField(
    # required=False, choices=('male', 'female'))


# class TokenPairSerializer(serializers.Serializer):
    # """
    # Serializer for refresh and access tokens
    # """
    #refresh = serializers.CharField()
    #access = serializers.CharField()
    #superuser = serializers.BooleanField()
    #jti = serializers.CharField()


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # """
    # Serializer to return tokens on login+password request
    # """
    # @classmethod
    # def get_token(cls, user):
    #token = super().get_token(user)

    # Add custom claims
    #token['superuser'] = user.is_superuser
    #token['jti'] = token.get('jti')
    # return token

    # def validate(self, attrs):
    #data = super().validate(attrs)
    #refresh = self.get_token(self.user)
    #data['refresh'] = str(refresh)
    #data['access'] = str(refresh.access_token)
    #data['superuser'] = refresh['superuser']
    #data['jti'] = str(refresh['jti'])
    # return data


# class LocationFullDataSerializer(serializers.Serializer):
    # """
    # Serializer for Location
    # """
    #uuid = serializers.UUIDField()
    #game = GameShortSerializer()
    #location_type = LocationTypeSerializer()
    #name = serializers.CharField()
    #short_name = serializers.CharField()
    #description = serializers.CharField()
    #hint = serializers.CharField()
    #number = serializers.IntegerField()
    #start_minutes = serializers.IntegerField()
    #finish_minutes = serializers.IntegerField()
    #photo_url = serializers.CharField()
    #point = PointSerializer()
    #radius = serializers.IntegerField()
    #active = serializers.BooleanField()
    #visible = serializers.BooleanField()
    #finish = serializers.BooleanField()
    #author = PlayerInfoSerializer()
    #task_list = TaskDataSerializer(read_only=True, many=True)


# class AuthorLocationFullDataSerializer(serializers.Serializer):
    # """
    # Serializer for Location
    # """
    #uuid = serializers.UUIDField()
    #game = GameShortSerializer()
    #location_type = LocationTypeSerializer()
    #name = serializers.CharField()
    #short_name = serializers.CharField()
    #description = serializers.CharField()
    #hint = serializers.CharField()
    #number = serializers.IntegerField()
    #start_minutes = serializers.IntegerField()
    #finish_minutes = serializers.IntegerField()
    #photo_url = serializers.CharField()
    #point = PointSerializer()
    #radius = serializers.IntegerField()
    #active = serializers.BooleanField()
    #visible = serializers.BooleanField()
    #finish = serializers.BooleanField()
    #author = PlayerInfoSerializer()
    #author_task_list = TaskDataSerializer(read_only=True, many=True)


# class GameHintsSerializer(serializers.Serializer):
    # """
    # Serializer for game hints
    # """
    #hints = serializers.ListSerializer(child=serializers.CharField())
