# chatapp/middleware.py
from django.shortcuts import redirect
from django.urls import reverse



class RedirectUnauthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
    
        allowed_paths = [
            reverse('login'),        
            reverse('register'),      
        ]

        # Check if user is authenticated and if the requested path is not allowed
        if not request.user.is_authenticated and request.path not in allowed_paths:
            return redirect('register')  # Redirect to login page if not authenticated

        response = self.get_response(request)
        return response