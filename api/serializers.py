from userprofile.models import UserProfile
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer
class UserProfileModelSerializer(ModelSerializer): 
    class Meta: 
        model = UserProfile
        fields = "__all__"