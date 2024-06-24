from email import message
import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message
import re

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_name = self.scope['url_route']['kwargs']['room_name']
        sanitized_room_name = re.sub(r'\W+', '', room_name)
        self.room_name = f"room_{sanitized_room_name}"
        
        if not self.room_name:
            await self.close()

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        await super().disconnect(code)

    async def receive(self, text_data):
        data_json = json.loads(text_data)
        event = {
            "type": "send_message",
            "message": data_json
        }

        await self.channel_layer.group_send(self.room_name, event)

    async def send_message(self, event):
        data = event["message"]
        await self.create_message(data)

        response = {
            "sender": data["sender"],
            "message": data["message"]
        }

        await self.send(text_data=json.dumps({"message": response}))

    @database_sync_to_async
    def create_message(self, data):
        get_room = Room.objects.get(room_name=data['room_name'])
        
        if not Message.objects.filter(message=data['message'], sender=data["sender"]).exists():
            Message.objects.create(room=get_room, message=data['message'], sender=data["sender"])
