# import necessary modules
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from channels.exceptions import StopConsumer

class MusicSocket(AsyncWebsocketConsumer):
    # connect the websocket
    async def connect(self):
        # get dynamic groupName
        self.group_name = self.scope['url_route']['kwargs']['groupName']
        self.user = self.scope['user']
        
        # Add group and channel together
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        # Broadcast a message that the user has joined
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'user_joined',
                'user': self.user.first_name  # Send user first name
            }
        )

        # Accept the connection
        await self.accept()

    # receive the message 
    async def receive(self, text_data):
        # Load the data into a Python dict
        message = json.loads(text_data)

        # Check if the message is an image
        if 'image' in message:
            # If it's an image, handle it separately
            await self.handle_image(message['image'])
        else:
            # Otherwise, it's a text message, broadcast it
            await self.channel_layer.group_send(
                self.group_name, {
                    'type': 'chat_message',
                    'text': message['text'],
                    'user': self.user.first_name  # Send the user's first name along with the message
                }
            )

    async def chat_message(self, event):
        # Extract the message and user from the event
        message = event['text']
        user = event['user']  # Get the user's first name

        # Send it to WebSocket
        await self.send(text_data=json.dumps({
            'text': message,
            'user': user  # Include the user's first name in the response
        }))

    # New method to handle image messages
    async def handle_image(self, image_data):
        # Broadcast the image to the group
        await self.channel_layer.group_send(
            self.group_name,
            {
                # assign task to image_message function
                'type': 'image_message',
                'image': image_data,  # Pass the image data
                'user': self.user.first_name  # Send the user's first name along with the image
            }
        )

    async def image_message(self, event):
        # Extract the image data and user from the event
        image_data = event['image']
        user = event['user']  # Get the user's first name

        # Send the image to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'image_message',  # Specify the type for the client to handle it
            'image': image_data,
            'user': user  # Include the user's first name in the response
        }))

    # Broadcast user join event
    async def user_joined(self, event):
        # Notify users of the new user who joined
        await self.send(text_data=json.dumps({
            'type': 'user_joined',
            'user': event['user']
        }))

    # Broadcast user leave event
    async def user_left(self, event):
        # Notify users when a user leaves
        await self.send(text_data=json.dumps({
            'type': 'user_left',
            'user': event['user']
        }))

    # disconnect the consumer 
    async def disconnect(self, code):
        # Broadcast a message that the user has left
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'user_left',
                'user': self.user.first_name
            }
        )
        
        # Remove the user from the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        raise StopConsumer()











