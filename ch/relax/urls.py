from django.urls import path
from .views import *

urlpatterns=[
    path('relax/<str:group_name>/', relax, name='relax'),
    path('invite/', invite_peoples,name='invite'),
    path('start_now/',start_now, name='start_now')
]

