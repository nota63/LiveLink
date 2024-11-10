# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Room
import os
from .models import Room, FileUpload
from django.core.files.storage import default_storage  # Import this
from .forms import MeetingForm


def join_room(request, room_name):
    room, created = Room.objects.get_or_create(name=room_name)
    return render(request, 'audio_channels/voice_channel.html', {'room_name': room_name})
@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        file_path = default_storage.save(f"uploads/{file.name}", file)
        file_url = default_storage.url(file_path)

        # Broadcast file to WebSocket
        room_name = request.POST.get("room_name")
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{room_name}",
            {
                "type": "file_share",
                "file_url": file_url,
                "filename": file.name
            }
        )

        return JsonResponse({"file_url": file_url, "filename": file.name})
    return JsonResponse({"error": "Invalid request"}, status=400)


def join_meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            # Create the meeting object but don't save it yet
            meet = form.save(commit=False)
            # Associate the meeting with the current user
            meet.user = request.user
            # Save the meeting to the database
            meet.save()
            # Redirect to the meeting_enter view with the meeting_link
            return redirect('meeting_enter', meeting_link=meet.meeting_link)  
    else:
        form = MeetingForm()  # Create an empty form instance

    return render(request, 'join_meeting.html', {'form': form})  # Render the form in the template

def meeting_enter(request):
    # Render the meeting page with the provided meeting link
    meeting_link='https://meet.zoho.in/82jYZigM58'
    return render(request, 'meeting.html', {'meeting_link': meeting_link})

def create_meeting(request):
    # Link to create a new Zoho Meeting
    create_meeting_link = "https://meeting.zoho.in/meeting/60033909493/948667000000008011/home"

    return render(request, 'create_meeting.html', {'create_meeting_link': create_meeting_link})
