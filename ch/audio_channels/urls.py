# urls.py
from django.urls import path
from .views import *
from .import views

urlpatterns = [
    path('upload_file/', upload_file, name='upload_file'),
    path('room/<str:room_name>/', join_room, name='join_room'),
    path('create_meeting/',create_meeting, name='create_meeting'),
    # path('join_meeting/', join_meeting, name='join_meeting'),
    # path('meeting_enter/<str:meeting_link>/', meeting_enter, name='meeting_enter'),
    path('join_meeting/', views.join_meeting, name='join_meeting'),
    path('meeting_enter/', views.meeting_enter, name='meeting_enter'),
    # ... other patterns
]