from userprofile.models import UserProfile
from futsal.models import Futsal, Booking, Contact
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer


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
