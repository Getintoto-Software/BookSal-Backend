import json
import math
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils.timezone import now
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

# Asynchronous function to interact with the database


@database_sync_to_async
def get_waiting_match(player_id, latitude, longitude, search_radius):
    for match in Matchmaking.objects.filter(status="waiting").exclude(player_id=player_id):
        distance = haversine(latitude, longitude,
                             match.latitude, match.longitude)
        if distance <= search_radius:
            return match
    return None


@database_sync_to_async
def create_matchmaking_entry(player_id, latitude, longitude):
    return Matchmaking.objects.create(player_id=player_id, latitude=latitude, longitude=longitude)


class MatchmakingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "matchmaking"
        self.room_group_name = f"ws_{self.room_name}"

        # Accept WebSocket connection
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        player_id = data["player_id"]
        latitude = float(data["latitude"])
        longitude = float(data["longitude"])
        status = data.get("status", "waiting")

        # Use sync_to_async to query the User model in an async context
        player = await sync_to_async(self.get_player)(player_id)

        if player is None:
            # Handle the case when player doesn't exist
            await self.send(text_data=json.dumps({"error": "Player does not exist"}))
            return

        # Now create the matchmaking entry
        match = Matchmaking.objects.create(
            player=player, latitude=latitude, longitude=longitude, status=status
        )

        # Send response back (e.g., matchmaking details)
        await self.send(text_data=json.dumps({
            "match_id": match.id,
            "player": match.player.username,
            "latitude": match.latitude,
            "longitude": match.longitude,
            "status": match.status,
            "created_at": match.created_at.isoformat(),
        }))

    async def disconnect(self, close_code):
        # Handle WebSocket disconnect
        pass

    # Synchronous method to retrieve player data
    def get_player(self, player_id):
        try:
            return User.objects.get(id=player_id)
        except ObjectDoesNotExist:
            return None
