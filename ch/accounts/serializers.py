from rest_framework import serializers
from .models import CustomUser


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
      model=CustomUser
      fields=['email','first_name','last_name','is_active','is_staff','joined_at']
      
    

