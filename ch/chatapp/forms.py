from django import forms
from .models import ChatIntialize, JoinChatRoom


class ChatInitializeForm(forms.ModelForm):
    class Meta:
        model=ChatIntialize
        fields='__all__'
        exclude=['created_at', 'user']



# join chat room form

class JoinChatRoomForm(forms.ModelForm):
    class Meta:
        model=JoinChatRoom
        fields='__all__'
        exclude=['user','date',]

        


