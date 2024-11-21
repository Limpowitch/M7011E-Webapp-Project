from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('recipes/<int:id>/', recipe_detail, name='recipe-detail'),
]