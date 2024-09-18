from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserProfileModelSerializer
from userprofile.models import UserProfile
# import listapi class from rest framework
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
#import session user
from django.contrib.auth.models import User


class UserProfileCreateView(CreateAPIView): 
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileModelSerializer
    permission_classes = [IsAuthenticated]
    
    
class UserProfileRetrieveView(RetrieveAPIView): 
    serializer_class = UserProfileModelSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'user'
    
    
    
    
class UserProfileUpdateView(UpdateAPIView): 
    # Only process the request if the user making the request is session user
    serializer_class = UserProfileModelSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user'
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    
    

    
class UserProfileDeleteView(DestroyAPIView): 
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileModelSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user'
    
class UserProfileListView(ListAPIView): 
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileModelSerializer
    permission_classes = [AllowAny]