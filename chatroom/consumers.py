from email import message
import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message
import re

class ChatConsumer(AsyncWebsocketConsumer):
    #connect method
    async def connect(self):
        # Get room name from URL kwargs
        room_name = self.scope['url_route']['kwargs']['room_name']
        
        # Sanitize room name
        sanitized_room_name = re.sub(r'\W+', '', room_name)  # Remove non-alphanumeric characters
        self.room_name = f"room_{sanitized_room_name}"
        
        # Check if sanitized room name is empty
        if not self.room_name:
            # Handle invalid room name
            await self.close()

        # Add channel to the group
        await self.channel_layer.group_add(self.room_name, self.channel_name)

        # Accept incoming WebSocket connection
        await self.accept()

    #disconnecting
    async def disconnect(self, code):
        # Remove channel from the group
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        await super().disconnect(code)

    #recieve messages
    async def receive(self, text_data):
        data_json = json.loads(text_data)
        #print(data_json)
    # Example: Echo the received message back to the client
        await self.send(text_data=json.dumps(data_json))
        event = {
            "type": "send_message",
            "message": data_json
        }

        await self.channel_layer.group_send(self.room_name,event)

    #creating message to database
    async def send_message(self,event):
        data = event["message"]
        await self.create_message(data = data)

        response = {
            "sender"  : data["sender"],
            "message": data["message"]
        }

        await self.send(text_data = json.dumps({"message":response}))

    @database_sync_to_async
    def create_message(self,data):
        get_room = Room.objects.get(room_name=data['room_name'])
        
        if not Message.objects.filter(message=data['message'],sender=data["sender"]).exists():
            new_message = Message.objects.create(room = get_room,message=data['message'],sender=data["sender"])

    