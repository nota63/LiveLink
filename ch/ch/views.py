from django.shortcuts import render, redirect
from audio_channels.forms import MeetingForm

def home(request):
    return render(request,'home.html')

def get_started(request):
    return render(request,'get_started.html')

