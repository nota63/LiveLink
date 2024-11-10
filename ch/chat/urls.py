from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),  # Homepage to join room
    path('room/', views.room, name='room'),  # Room page where video call happens
    path('guide/',views.guide, name='guide'),
    path('how/',views.how_it_works, name='how'),
    path('support/', views.support, name='support'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy')
]

