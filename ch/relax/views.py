from django.shortcuts import render, redirect
import pygame
from .forms import InviteForm
from.models import Invite
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# Create your views here.



# start now
def start_now(request):
    return render(request,'relax/start_now.html')




# create a func to invite peoples in the room
def invite_peoples(request):
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            form.save()

            # Getting emails of all selected users
            selected_users = form.cleaned_data['users']
            recipient_list = [user.email for user in selected_users]

            if instance.another_email:
                recipient_list.append(instance.another_email)

            # Compose email subject and content
            subject = f'Invitation to Join! Live Room: {instance.group_name}'
            user=request.user.first_name
            
            # Render the email message using HTML
            message_html = render_to_string('relax/invite_email.html', {
                'group_name': instance.group_name,
                'user':user,
                'room_link': f'http://127.0.0.1:8000/relax/invite/{instance.group_name}',
            })

            from_email = settings.DEFAULT_FROM_EMAIL

            # Send email with HTML content
            email = EmailMessage(subject, message_html, from_email, recipient_list)
            email.content_subtype = 'html'  # Set the content to HTML
            email.send()

            return redirect('relax',group_name=instance.group_name)  # Redirect or success page after sending emails
    else:
        form = InviteForm()

    return render(request, 'relax/invite.html', {'form': form})






def relax(request, group_name):
 
    # Ensure that the group_name is passed to the template
    return render(request, 'relax/relax.html', {
        'group_name': group_name
    })
    # play_audio_non_stop('calm-night.mp3')



# function to play audio continiously
def play_audio_non_stop(audio_file):
    # Initialize the pygame mixer
    pygame.mixer.init()

    # Load the audio file
    pygame.mixer.music.load(audio_file)

    # Play the audio on loop (-1 means infinite loop)
    pygame.mixer.music.play(-1)

    # Keep the program running to allow the audio to play
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Small delay to avoid high CPU usage

# Example usage
# play_audio_non_stop('calm-night.mp3')


