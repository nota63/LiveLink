from django.db import models
from accounts.models import CustomUser
# Create your models here.
# create model to invite peoples in the room


class Invite(models.Model):
    group_name=models.CharField(max_length=250)
    users=models.ManyToManyField(CustomUser,related_name='invited_users')
    another_email=models.EmailField(blank=True, null=True)

    