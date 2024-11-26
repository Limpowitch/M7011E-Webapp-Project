from django.urls import path
from .views import *

urlpatterns = [
    path('authenticate/', authenticate_user, name='authenticate_user'),
]