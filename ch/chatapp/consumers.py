import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user = self.scope['user']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Notify the group that a user has joined
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'user_joined',
            'email': self.user.first_name,  # Correctly pass the email
        })

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Notify the group that a user has left
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'user_left',
            'email': self.user.first_name,  # Correctly pass the email
        })

    async def receive(self, text_data):
        data = json.loads(text_data)

        if 'message' in data:
            message = data['message']
            email = self.user.first_name
            
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                'email': email,  # Send the email correctly
            })

        elif 'typing' in data:
            # Send typing indicator to group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'typing_indicator',
                'email': self.user.first_name,  # Pass correct email
            })

    async def user_joined(self, event):
        email = event['email']  # Get the email from the event
        # Broadcast a message indicating that a user has joined
        await self.send(text_data=json.dumps({
            'user_joined': f"{email} has joined the room.",
            'email': email,  # Pass the email to the frontend
        }))

    async def user_left(self, event):
        email = event['email']  # Get the email from the event
        # Broadcast a message indicating that a user has left
        await self.send(text_data=json.dumps({
            'user_left': f"{email} has left the room.",
            'email': email,  # Pass the email to the frontend
        }))

    async def chat_message(self, event):
        message = event['message']
        email = event['email']  # Get the email from the event
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'email': email,  # Send the email for the frontend to display
        }))

    async def typing_indicator(self, event):
        email = event['email']  # Get the email from the event
        # Send typing indicator to WebSocket
        await self.send(text_data=json.dumps({
            'typing': f"{email} is typing...",
            'email': email,  # Pass correct email
        }))
