from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserProfileModelSerializer
from .serializers import FutsalModelSerializer, BookingModelSerializer
from userprofile.models import UserProfile
from futsal.models import Futsal, Booking
# import listapi class from rest framework
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
# import session user
from django.contrib.auth.models import User

# User Profile Views


class UserProfileCreateAPIView(CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileModelSerializer
    permission_classes = [IsAuthenticated]


class UserProfileRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserProfileModelSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'user'


class UserProfileUpdateAPIView(UpdateAPIView):
    # Only process the request if the user making the request is session user
    serializer_class = UserProfileModelSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user'

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class UserProfileDeleteAPIView(DestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileModelSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user'


class UserProfileListAPIView(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileModelSerializer
    permission_classes = [AllowAny]


# Futsal Views
class FutsalListAPIView(ListAPIView):
    queryset = Futsal.objects.all()
    serializer_class = FutsalModelSerializer
    permission_classes = [AllowAny]


class FutsalCreateAPIView(CreateAPIView):
    queryset = Futsal.objects.all()
    serializer_class = FutsalModelSerializer
    permission_classes = [IsAuthenticated]


class FutsalRetrieveAPIView(RetrieveAPIView):
    queryset = Futsal.objects.all()
    serializer_class = FutsalModelSerializer
    permission_classes = [AllowAny]


class FutsalUpdateAPIView(UpdateAPIView):
    queryset = Futsal.objects.all()
    serializer_class = FutsalModelSerializer
    permission_classes = [IsAuthenticated]


class FutsalDeleteAPIView(DestroyAPIView):
    queryset = Futsal.objects.all()
    serializer_class = FutsalModelSerializer
    permission_classes = [IsAuthenticated]

# Booking Views


class BookingListAPIView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingModelSerializer
    permission_classes = [AllowAny]


class BookingCreateAPIView(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingModelSerializer
    permission_classes = [IsAuthenticated]


class BookingRetrieveAPIView(RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingModelSerializer
    permission_classes = [AllowAny]


class BookingUpdateAPIView(UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingModelSerializer
    permission_classes = [IsAuthenticated]


class BookingDeleteAPIView(DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingModelSerializer
    permission_classes = [IsAuthenticated]
