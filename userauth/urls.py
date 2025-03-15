from django.urls import path, include
from .views import *

app_name = "userauths"

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
]