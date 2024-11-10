from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# import email


# Create your models here.


class ChatIntialize(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    room_name=models.CharField(max_length=100)
    emails=models.TextField(max_length=10000, null=True, blank=True)
    created_at=models.DateTimeField(auto_now=True)



# create model to join room

class JoinChatRoom(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    room_title=models.CharField(max_length=100)
    date_joined=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.room_title}'
    
    



