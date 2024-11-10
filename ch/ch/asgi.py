"""
ASGI config for ch project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import chatapp.routing  # Import routing from your chat app  # Import your VideoChat consumer
from django.urls import path
import chat.routing
import relax.routing
import audio_channels.routing
# Set the default settings module for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')  # Change to your project name
from channels.auth import AuthMiddlewareStack
# Create the ASGI application
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chatapp.routing.ws_urlpatterns + chat.routing.websocket_urlpatterns+relax.routing.websocket_urlpatterns+audio_channels.routing.websocket_urlpatterns
        )
    ),
})