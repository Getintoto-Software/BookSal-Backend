from userprofile.models import UserProfile
from rest_framework.serializers import ModelSerializer

class UserProfileModelSerializer(ModelSerializer): 
    class Meta: 
        model = UserProfile
        fields = "__all__"
        
