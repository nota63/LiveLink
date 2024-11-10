from django.shortcuts import render, redirect
from .models import ChatIntialize, JoinChatRoom
from .forms import ChatInitializeForm, JoinChatRoomForm
from django.http import JsonResponse
import time
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import ChatInitializeForm
from .models import ChatIntialize
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf.global_settings import DEFAULT_FROM_EMAIL

# create chat function
@login_required
def create_chat_room(request):
    if request.method == 'POST':
        form = ChatInitializeForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.user = request.user
            room.save()

            # Send email to the user with room details directly within the same function
            subject = f'Join the Chat Room: {room.room_name} - Invitation from {room.user.first_name}'

            # Define the HTML message directly
            html_message = f"""
            <html>
<head>
    <style>
        body {{
            font-family: 'Poppins', sans-serif;
            background-color: #f4f7fb;
            color: #333;
            padding: 20px;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            padding: 30px;
            text-align: center;
        }}
        h1 {{
            color: #007bff;
            font-size: 28px;
            margin-bottom: 20px;
        }}
        p {{
            font-size: 16px;
            line-height: 1.6;
            color: #555;
        }}
        a {{
            color: #fff;
            background-color: #007bff;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            font-size: 16px;
        }}
        a:hover {{
            background-color: #0056b3;
        }}
        .footer {{
            margin-top: 30px;
            font-size: 14px;
            color: #888;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>You've Been Invited to Join a Chat Room!</h1>
        <p>Hi,</p>
        <p>{room.user.first_name} has created a chat room and would like you to join the conversation.</p>
        <p>The room, <strong>{room.room_name}</strong>, offers a seamless, real-time communication experience. Enjoy encrypted and secure conversations with your friends, family, or colleagues in a modern, professional environment.</p>
        <p>Click the button below to join the chat room:</p>
        <p><a href="http://127.0.0.1:8000/create_chat_room/join_chat/{room.room_name}/">Join Chat Room</a></p>
        <p>You can rejoin the room anytime. We look forward to seeing you there!</p>
        
        <div class="footer">
            <p>Thank you for choosing <strong>LiveLink</strong> – your go-to platform for secure and dynamic live interactions!</p>
        </div>
    </div>
</body>
</html>
            """

            # Define the plain text version of the message
            plain_message = f"""
            Hi,

            {room.user.first_name} has invited you to join the chat room '{room.room_name}'. 
            
            Feel free to join using the link below:

            http://127.0.0.1:8000/create_chat_room/join_chat/{room.room_name}/

            We look forward to having you in the chat room.

            Thank you for using LiveLink – your solution for real-time communication!
            """

            from_email ='your-email@gmail.com'
          # Split the comma-separated string into a list of email addresses
            recipient_list = [email.strip() for email in room.emails.split(',') if email.strip()]# The email address entered in the form

            # Send the email using Django's send_mail function
            send_mail(
                subject,
                plain_message,
                from_email,
                recipient_list,
                html_message=html_message
            )

            return redirect('join_chat', room_name=room.room_name)
    else:
        form = ChatInitializeForm()

    # Get the current time and format it correctly
    t = time.localtime()
    actual_time = time.strftime('%d-%m-%y %H:%M:%S', t)

    # Render the form and pass the actual time to the template
    return render(request, 'chatapp/create_chatroom.html', {'form': form, 'actual_time': actual_time})


# imports for contextual suggestions
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import json

# Set up OpenAI API key
openai.api_key = "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"

# create a function to handle contextual suggestions
def get_room_suggetions(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        context = data.get('context', '')

        # Call OpenAI API to get room name suggestions
        prompt = f"Suggest creative and unique room names for the {context} theme."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates room name suggestions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50
        )

        # Extract suggestions from the response
        suggestions_text = response.choices[0].message['content']
        
        # Split suggestions text into a list if needed (assuming suggestions are comma-separated or line-separated)
        suggestions = [s.strip() for s in suggestions_text.split('\n') if s.strip()]

        # Return suggestions as JsonResponse
        return JsonResponse(suggestions, safe=False)
    
    return JsonResponse({"error": "Invalid request"}, status=400)+






@login_required
def join_room_chat(request):
    if request.method == 'POST':
        form=JoinChatRoomForm(request.POST)
        if form.is_valid():
            try:
              join=form.save(commit=False)
              join.user=request.user
              join.save()
            except Exception as e:
                return JsonResponse({'alert':str(e)}, status=400)
            messages.success(request,f'Room {join.room_title} Joined Successfully')
            return redirect('join_chat',room_name=join.room_title)
    else:
        form=JoinChatRoomForm()
    t = time.localtime()
    actual_time = time.strftime('%d-%m-%y %H:%M:%S', t)        
    return render(request,'chatapp/join_room_chat.html',{'form':form,'actual_time':actual_time})


@login_required
def join_chat(request, room_name):
    return render(request, 'chatapp/join_room.html', {"room_name": room_name})


# chats database area starts
@login_required
def created_chat_rooms(request):
    rooms=ChatIntialize.objects.filter(user=request.user)
    return render(request,'chatapp/created_chat_rooms.html',{'rooms':rooms})

@login_required
def delete_chat_rooms(request):
    rooms=ChatIntialize.objects.filter(user=request.user)

    if rooms.exists:
        rooms.delete()
        messages.success(request,'All Entries Has Been Deleted')
    else:
        messages.warning(request,'No Chat Rooms Found To Delete!')
    return redirect('created_chat_rooms')

@login_required
def joined_chat_rooms(request):
    joined=JoinChatRoom.objects.filter(user=request.user)
    return render(request,'chatapp/joined_chat_rooms.html',{'joined':joined})
        
@login_required
def clear_joined_rooms(request):
    rooms=JoinChatRoom.objects.filter(user=request.user)
    try:
        if rooms.exists:
            rooms.delete()
            messages.success(request,'All Entries Deleted Successfully!')
        else:
            messages.warning(request,'Nothing To Delete!')
        return redirect('joined_chat_rooms')   
    except Exception as e:
        return JsonResponse({'msg':str(e)}, status=400)
                        