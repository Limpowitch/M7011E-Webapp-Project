from django.urls import path
from .views import *
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account_api'),
]