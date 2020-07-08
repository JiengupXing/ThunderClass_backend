from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name="user_login"),
    path('register/', register, name="user_register"),
]