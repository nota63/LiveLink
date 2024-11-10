from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, LoginForm

# Registration View
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import datetime
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import datetime

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Extracting username and password (password is hashed, so send raw password from form data)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')  # assuming 'password1' is the password field

            # Email content
            subject = 'Welcome to LiveLink - Your Account Details'
            message = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Welcome Email</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        color: #333333;
                        margin: 0;
                        padding: 20px;
                    }}
                    .email-container {{
                        background-color: #ffffff;
                        border-radius: 10px;
                        box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
                        padding: 25px;
                        max-width: 650px;
                        margin: auto;
                    }}
                    .email-header {{
                        background-color: #1E88E5;
                        padding: 15px;
                        text-align: center;
                        border-top-left-radius: 10px;
                        border-top-right-radius: 10px;
                        color: #ffffff;
                    }}
                    .email-content {{
                        padding: 20px;
                        font-size: 16px;
                        line-height: 1.8;
                        color: #555555;
                    }}
                    .email-content h2 {{
                        color: #1E88E5;
                    }}
                    .credentials {{
                        background-color: #f1f1f1;
                        padding: 15px;
                        border-radius: 8px;
                        font-size: 14px;
                        margin: 20px 0;
                    }}
                    .email-footer {{
                        margin-top: 30px;
                        text-align: center;
                        font-size: 12px;
                        color: #888888;
                    }}
                    .button {{
                        display: inline-block;
                        padding: 12px 25px;
                        background-color: #1E88E5;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                        margin-top: 20px;
                    }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="email-header">
                        <h1>Welcome to LiveLink, {user.first_name}!</h1>
                    </div>
                    <div class="email-content">
                        <h2>Hello {user.first_name},</h2>
                        <p>
                            We are thrilled to welcome you to LiveLink, the platform where real-time conversations and video calls come to life.
                        </p>
                        <p>
                            You can now connect with others, send instant messages, and make seamless video calls, all within our secure platform. 
                        </p>
                        <h3>Your Account Details</h3>
                        <div class="credentials">
                            <p><strong>Email:</strong> {user.email}</p>
                            <p><strong>Password:</strong> {raw_password}</p>
                        </div>
                        <p>
                            For security reasons, we recommend changing your password after your first login. You can easily do this from your account settings.
                        </p>
                        <p style="text-align: center;">
                            <a href="https://www.livelink.com/login" class="button">Access Your Account</a>
                        </p>
                        <p>
                            If you have any questions or need assistance, our support team is always here to help.
                        </p>
                        <p>Best Regards,</p>
                        <p>The LiveLink Team</p>
                    </div>
                    <div class="email-footer">
                        <p>&copy; {datetime.now().year} LiveLink. All rights reserved.</p>
                        <p>This email was sent to {user.email}. If you didn’t create this account, please contact us immediately.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            # Send email
            email = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            email.content_subtype = 'html'  # Important to tell Django to send the email as HTML
            email.send()

            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Login View
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

# Logout View
# @login_required
# def user_logout(request):
#     logout(request)
#     return redirect('login')

def user_logout(request):
    if request.method == 'POST':
      logout(request)
      return redirect('home')
    return render(request,'accounts/logout.html')



# set up RestAPI
from .serializers import UsersSerializer
from .models import CustomUser
from rest_framework import viewsets, throttling
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework.pagination import PageNumberPagination
from .pagination import CustomPagination

# create custom throttle class
class CustomAnonRateThrottle(throttling.UserRateThrottle):
    # set the rate for 2 requests per minute
    rate='2/min'



# create a viewset
class UsersSet(viewsets.ModelViewSet):
    queryset=CustomUser.objects.all()
    serializer_class=UsersSerializer
    authentication_classes=[SessionAuthentication]
    permission_classes=[DjangoModelPermissions,IsAdminUser]
    throttle_classes=[UserRateThrottle,AnonRateThrottle]
    pagination_class=CustomPagination



