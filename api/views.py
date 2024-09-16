from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserProfileModelSerializer
from userprofile.models import UserProfile
# import listapi class from rest framework
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

class UserProfileCreateView(CreateAPIView): 
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileModelSerializer
    permission_classes = [IsAuthenticated]