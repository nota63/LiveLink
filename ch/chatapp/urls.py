from django.urls import path
from .views import *

urlpatterns=[
    path('create_chat_room/', create_chat_room, name='create_chat_room'),
    path('join_chat/<str:room_name>/', join_chat, name='join_chat'),
    path('join_room_chat/', join_room_chat, name='join_room_chat'),
    path('created_chat_rooms/', created_chat_rooms, name='created_chat_rooms'),
    path('delete_chat_rooms/', delete_chat_rooms, name='delete_chat_rooms'),
    path('joined_chat_rooms/', joined_chat_rooms, name='joined_chat_rooms'),
    path('clear_joined_rooms/', clear_joined_rooms, name='clear_joined_rooms'),
    path('get-room-suggetions/', get_room_suggetions, name='get-room-suggetions')
]
