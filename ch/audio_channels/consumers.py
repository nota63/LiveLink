# consumers.py
# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")
        file_url = data.get("file_url")
        filename = data.get("filename")

        # Send the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "file_share",  # Now using a single 'chat_message' type
                "message": message,
                "file_url": file_url,
                "filename": filename,
            }
        )

    async def file_share(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": event.get("message"),
            "file_url": event.get("file_url"),
            "filename": event.get("filename")
        }))