from django.urls import re_path
from . import consumers  # Import the consumers file where MusicSocket is defined

# routing.py
from django.urls import re_path
from . import consumers  # Import your consumers

websocket_urlpatterns = [
    re_path(r'ws/music/(?P<groupName>\w+)/$', consumers.MusicSocket.as_asgi()),  # Captures the dynamic groupName
]
