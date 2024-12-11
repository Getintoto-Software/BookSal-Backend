from userprofile.models import UserProfile
from futsal.models import Futsal, Booking
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer


class UserProfileModelSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class FutsalModelSerializer(ModelSerializer):
    class Meta:
        model = Futsal
        fields = "__all__"


class BookingModelSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
