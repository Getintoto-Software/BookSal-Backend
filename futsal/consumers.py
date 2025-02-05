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


class MatchmakingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = "matchmaking"
        # self.room_group_name = f"ws_{self.room_name}"
        # await self.accept()

        self.room_group_name = "matchmaking"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        if action == "join_room":
            player_id = data.get("player_id")
            room_id = data.get("room_id")

            if not player_id or not room_id:
                await self.send(text_data=json.dumps({"error": "Missing player_id or room_id"}))
                return

            match = await database_sync_to_async(Matchmaking.objects.filter(id=room_id, player_2_id=None).first)()

            if match:
                match.player_2_id = player_id
                match.status = "matched"
                await database_sync_to_async(match.save)()

                # Notify both players
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "match_found",
                        "room_id": match.id,
                        "player_1_id": match.player_1_id,
                        "player_2_id": match.player_2_id,
                        "message": f"Match joined successfully in Room {match.id}",
                    },
                )
            else:
                await self.send(text_data=json.dumps({"error": "Room already full or not found"}))

    @database_sync_to_async
    def get_user(self, player_id):
        """ Fetch the user from the database """
        try:
            return User.objects.get(pk=player_id)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def find_waiting_match(self, player_id, latitude, longitude, search_radius):
        """ Find a waiting matchmaking entry within the search radius """
        matches = Matchmaking.objects.filter(
            status="waiting", player_2__isnull=True).exclude(player_1_id=player_id)
        for match in matches:
            if haversine(latitude, longitude, match.latitude, match.longitude) <= search_radius:
                return match
        return None

    @database_sync_to_async
    def update_match(self, match, player_2):
        """ Update an existing match with player_2 and change status to matched """
        match.player_2 = player_2
        match.status = "matched"
        match.is_active = False
        match.save()
        return match

    @database_sync_to_async
    def create_matchmaking_entry(self, player_1, latitude, longitude):
        """ Create a new matchmaking entry """
        return Matchmaking.objects.create(player_1=player_1, latitude=latitude, longitude=longitude)

    async def disconnect(self, close_code):
        """ Handle WebSocket disconnection """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
