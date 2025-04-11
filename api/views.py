from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserProfileModelSerializer, UserModelSerializer
from .serializers import FutsalModelSerializer, BookingModelSerializer, BookingReadModelSerializer, ContactModelSerializer, MatchmakingRoomSerializer
from userprofile.models import UserProfile
from futsal.models import Futsal, Booking, Contact, Matchmaking
# import listapi class from rest framework
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
# import session user
from django.contrib.auth.models import User

# API For matchmaking
from django.db.models import F, Func, FloatField, Value
from django.http import JsonResponse
import math

# API for booking management
from .serializers import UserBookingModelSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from math import radians, sin, cos, sqrt, atan2


# API for blog management
from .serializers import BlogPostModelSerializer
from blog.models import  BlogPost

class BlogPostListAPIView(ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostModelSerializer
    permission_classes = [AllowAny]
    
class BlogPostRetrieveAPIView(RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostModelSerializer
    permission_classes = [AllowAny]

class MatchmakingListAPIView(ListAPIView):
    queryset = Matchmaking.objects.filter(
        is_active=True)  # Only active rooms
    serializer_class = MatchmakingRoomSerializer


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


class UserBookingsListAPIView(ListAPIView):
    serializer_class = UserBookingModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.kwargs['user'])


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

# Change this queryset to only render bookings of a certain futsal at a time.
# reduce the load on the server.


class BookingListAPIView(ListAPIView):
    serializer_class = BookingReadModelSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Booking.objects.filter(futsal=self.kwargs['pk'])


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


class ContactCreateAPIView(CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactModelSerializer
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


# For Matchmaking
PLAYERS_CACHE_KEY = "waiting_players"
if not cache.get(PLAYERS_CACHE_KEY):
    cache.set(PLAYERS_CACHE_KEY, [], timeout=None)


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the distance between two geographic points in km."""
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * \
        cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c


class FindMatchAPIView(APIView):
    def post(self, request):
        """Find the closest available player and pair them."""
        user_id = request.data.get("user_id")
        user_lat = float(request.data.get("latitude"))
        user_lon = float(request.data.get("longitude"))

        players = cache.get(PLAYERS_CACHE_KEY, [])

        # If the queue is empty, inform the user.
        if not players:
            return Response({"message": "No players in the queue. Please wait for others."}, status=status.HTTP_200_OK)

        # Add user to queue if they are not already in it
        if not any(p["user_id"] == user_id for p in players):
            players.append(
                {"user_id": user_id, "latitude": user_lat, "longitude": user_lon})
            cache.set(PLAYERS_CACHE_KEY, players, timeout=None)
            print(players)

        # Find the closest available player
        closest_player = None
        min_distance = float("inf")

        for player in players:
            if player["user_id"] != user_id:
                distance = haversine_distance(
                    user_lat, user_lon, player["latitude"], player["longitude"])
                if distance < min_distance:
                    min_distance = distance
                    closest_player = player

        if closest_player:
            return Response(
                {"message": "Match found!", "matched_with": closest_player["user_id"], "distance_km": round(
                    min_distance, 2)},
                status=status.HTTP_200_OK,
            )

        return Response({"message": "No nearby players found. Waiting for match."}, status=status.HTTP_200_OK)


class JoinMatchAPIView(APIView):
    def post(self, request):
        """Confirm a match between two players and remove them from the waiting list."""
        user_id = request.data.get("user_id")
        matched_user_id = request.data.get("matched_user_id")

        players = cache.get(PLAYERS_CACHE_KEY, [])

        # Remove both users from the queue
        updated_players = [p for p in players if p["user_id"]
                           not in [user_id, matched_user_id]]
        cache.set(PLAYERS_CACHE_KEY, updated_players, timeout=None)

        return Response({"message": "Match confirmed!", "players": [user_id, matched_user_id]}, status=status.HTTP_200_OK)


class LeaveQueueAPIView(APIView):
    def post(self, request):
        """Remove a user from the waiting queue."""
        user_id = request.data.get("user_id")
        players = cache.get(PLAYERS_CACHE_KEY, [])
        updated_players = [p for p in players if p["user_id"] != user_id]
        cache.set(PLAYERS_CACHE_KEY, updated_players, timeout=None)
        return Response({"message": "Left the queue successfully"}, status=status.HTTP_200_OK)
