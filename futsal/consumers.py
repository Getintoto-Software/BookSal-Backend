import json
import math
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from .models import Matchmaking
from asgiref.sync import sync_to_async

# Haversine Formula to calculate distance between two lat/lng points


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) ** 2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon/2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c


class MatchmakingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "matchmaking"
        # Join the group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        if action == "find_match":
            player_id = data.get("player_id")
            latitude = data.get("latitude")
            longitude = data.get("longitude")
            search_radius = data.get("radius")

            # Try to find an existing match
            match = await self.get_waiting_match(player_id, latitude, longitude, search_radius)

            if match:
                # Send match found
                await self.send(text_data=json.dumps({
                    "type": "match_found",
                    "room_id": match.id,
                    "player_1_username": match.player_1.username,
                    "player_2_username": match.player_2.username,
                }))
            else:
                # Create a new matchmaking entry if no match found
                new_match = await self.create_matchmaking_entry(player_id, latitude, longitude)
                await self.send(text_data=json.dumps({
                    "type": "match_created",
                    "room_id": new_match.id,
                    "message": "Matchmaking room created successfully!"
                }))

        elif action == "join_match":
            room_id = data.get("room_id")
            player_id = data.get("player_id")
            latitude = data.get("latitude")
            longitude = data.get("longitude")

            # Try to join an existing match as player_2
            match = await self.get_match_by_id(room_id)
            if match and match.player_2 is None:
                player_2 = await self.get_user(player_id)
                if player_2:
                    match = await self.update_match(match, player_2)
                    await self.send(text_data=json.dumps({
                        "type": "match_joined",
                        "room_id": match.id,
                        "player_2_username": match.player_2.username,
                        "message": "You have joined the match as Player 2!"
                    }))
                else:
                    await self.send(text_data=json.dumps({
                        "type": "error",
                        "message": "Player not found!"
                    }))
            else:
                await self.send(text_data=json.dumps({
                    "type": "error",
                    "message": "Match not found or already full!"
                }))

    @database_sync_to_async
    def get_user(self, player_id):
        """ Fetch the user from the database """
        try:
            return User.objects.get(pk=player_id)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def get_waiting_match(self, player_id, latitude, longitude, search_radius):
        """ Find a waiting matchmaking entry within the search radius """
        matches = Matchmaking.objects.filter(
            status="waiting", player_2__isnull=True).exclude(player_1_id=player_id)
        for match in matches:
            if haversine(latitude, longitude, match.latitude, match.longitude) <= search_radius:
                return match
        return None

    @database_sync_to_async
    def get_match_by_id(self, room_id):
        """ Get a matchmaking room by its ID """
        try:
            return Matchmaking.objects.get(id=room_id)
        except Matchmaking.DoesNotExist:
            return None

    @database_sync_to_async
    def update_match(self, match, player_2):
        """ Update an existing match with player_2 and change status to matched """
        match.player_2 = player_2
        match.status = "matched"
        match.is_active = False
        match.save()
        return match

    @staticmethod
    @database_sync_to_async
    def create_matchmaking_entry(player_id, latitude, longitude):
        """ Create a new matchmaking entry in the database """
        return Matchmaking.objects.create(
            player_1_id=player_id,
            latitude=latitude,
            longitude=longitude,
            status="waiting"
        )

    async def disconnect(self, close_code):
        """ Handle WebSocket disconnection """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
