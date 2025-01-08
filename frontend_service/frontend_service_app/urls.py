from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('recipes/<int:id>/', recipe_detail, name='recipe-detail'),
    path('category/<str:category>', category, name='category'), 
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create_recipe/', create_recipe, name='create_recipe'),
    path('register/', register, name='register'),
    path('change-password/', change_password, name='change_password'),
    path('delete-account/', delete_account, name='delete_account'),
    path('verify_2fa/', two_way_auth_view, name='verify_2fa'),
    path('user_information', user_information, name='user_information'),
    path('edit_recipe/<int:id>/', edit_recipe, name='edit_recipe'),
    path('delete_recipe/<int:id>/', delete_recipe, name='delete_recipe'),
    path('admin_page/', admin_view, name='admin_page'),
    path('approve_recipe/<int:id>/', approve_recipe, name='approve_recipe'),
    path('administrate_users', administrate_users, name='administrate_users'),
    path('change_to_superuser/<int:id>', change_to_superuser, name='change_to_superuser'),




]