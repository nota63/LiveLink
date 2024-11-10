from django.urls import path, include
from .views import register, user_login, user_logout
# api urls

from rest_framework.routers import DefaultRouter
from .views import UsersSet


router=DefaultRouter()
router.register(r'users',UsersSet)



urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('users',include(router.urls))
]
