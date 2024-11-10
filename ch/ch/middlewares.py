from django.shortcuts import redirect, render


class ComingSoonMiddleware:
    PATHS=('/guide/how', '/guide/support','/guide/privacy_policy/')
    def __init__(self, get_response):
        self.get_response= get_response

    def __call__(self, request):

        if any(request.path.startswith(path) for path in self.PATHS):
            return render(request,'chat/coming_soon.html')

        response=self.get_response(request)
        return response    
    
from django.core.cache import cache
import time

from django.http import HttpResponseForbidden

class ThrottleCheck:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the response from the view or next middleware
        response = self.get_response(request)
        
        # Call the IP check after getting the response
        return self.check_ip(response, request)

    def check_ip(self, response, request):
        # Get user's IP address from the request
        user_ip = request.META.get('REMOTE_ADDR')
        
    
        count = cache.get(user_ip, 0)
   
        if count > 100:
            return render(request,'throttle.html',{'user_ip':user_ip,'count':count})
        
     
        cache.set(user_ip, count + 1, timeout=60)
        
      
        return response
           

class IpCheckMiddleware:
    ALLOWED_IPS=['203.0.113.45','127.0.0.1']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
       
        if request.path.startswith('/admin'):
        
            user_ip=request.META.get('REMOTE_ADDR')
          
            if user_ip not in self.ALLOWED_IPS:
                return render(request,'admin_deny.html',{"user_ip":user_ip})
            return self.get_response(request)
        return self.get_response(request)
    


