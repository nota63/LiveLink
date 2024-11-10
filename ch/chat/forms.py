from django import forms
from .models import Room


# room form

class RoomForm(forms.ModelForm):
    class Meta:
        model=Room
        fields='__all__'
        exclude=['created_at']

        
