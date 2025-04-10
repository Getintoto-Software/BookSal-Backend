from userprofile.models import UserProfile
from futsal.models import Futsal, Booking, Contact, Matchmaking
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer
from rest_framework import serializers


class MatchmakingRoomSerializer(serializers.ModelSerializer):
    player1_username = serializers.CharField(
        source="player_1.username", read_only=True)
    player2_username = serializers.CharField(
        source="player_2.username", read_only=True)

    class Meta:
        model = Matchmaking
        fields = ['id', 'player_1', 'player1_username', 'player_2',
                  'player2_username', 'created_at', 'is_active']


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class UserProfileModelSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class FutsalModelSerializer(ModelSerializer):
    class Meta:
        model = Futsal
        fields = "__all__"


class UserBookingModelSerializer(ModelSerializer):
    user = UserModelSerializer(read_only=True)
    futsal = FutsalModelSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "user", "futsal", "booking_date",
                  "booking_start_time", "booking_end_time"]


class BookingModelSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"


class BookingReadModelSerializer(ModelSerializer):
    user = UserModelSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"


class ContactModelSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class FindMatchSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class JoinMatchSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
    matched_user_id = serializers.CharField(max_length=100)


class LeaveQueueSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
