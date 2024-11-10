from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    room_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
