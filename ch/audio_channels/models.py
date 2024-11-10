from django.db import models
from accounts.models import CustomUser
from django.contrib.auth.models import User
# Create your models here.
# model for implement room and track the room \\
class Room(models.Model):
    name=models.CharField(max_length=100, unique=True)
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# model to upload files
class FileUpload(models.Model):
    # foreignkey to room
    room=models.ForeignKey(Room, on_delete=models.CASCADE, related_name='uploads')
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.filename} in {self.room.name}"
    

class Meeting(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)  
    meeting_link=models.CharField(max_length=100000)
