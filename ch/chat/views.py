from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm
from django.contrib import messages

def index(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room_name = form.cleaned_data['room_name']  # Get the room name from the form
            return redirect('room', room_name=room_name)  # Redirect to the room with the entered room name
    else:
        form = RoomForm()

    return render(request, 'chat/index.html', {'form': form})


def guide(request):
    return render(request,'chat/guide.html')


def room(request):
    # Render the room template with the room name so users can interact live
    return render(request, 'chat/room.html')


def how_it_works(request):
    return render(request,'chat/how.html')

def support(request):
    return render(request,'chat/support.html')

def privacy_policy(request):
    pass