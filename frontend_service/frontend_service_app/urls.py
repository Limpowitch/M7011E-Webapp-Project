from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('recipes/<int:id>/', recipe_detail, name='recipe-detail'),
    path('category/<str:category>', category, name='category'), 
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]