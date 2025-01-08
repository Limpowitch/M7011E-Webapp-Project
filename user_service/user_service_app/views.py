from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError

class RegisterView(APIView):
    def post(self, request):
        data = request.data

        username = data.get('username')
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password1 = data.get('password1')
        password2 = data.get('password2')

        if not username or not email or not password1 or not password2:
            return Response({'errors': {'detail': 'All fields are required.'}}, status=status.HTTP_400_BAD_REQUEST)

        if password1 != password2:
            return Response({'errors': {'password': 'Passwords do not match.'}}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(password1) 
        except ValidationError as e:
            return Response({'errors': {'password': e.messages}}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'errors': {'username': 'Username already exists.'}}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'errors': {'email': 'Email already exists.'}}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password1)
        return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)

class ChangePasswordView(APIView):
    def post(self, request):
        user = request.user
        data = request.data

        current_password = data.get('current_password')
        new_password1 = data.get('new_password1')
        new_password2 = data.get('new_password2')

        if not current_password or not new_password1 or not new_password2:
            return Response({'errors': {'detail': 'All fields are required.'}}, status=status.HTTP_400_BAD_REQUEST)

        if new_password1 != new_password2:
            return Response({'errors': {'new_password': 'Passwords do not match.'}}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(current_password):
            return Response({'errors': {'current_password': 'Current password is incorrect.'}}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password1)
        user.save()
        return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)

class DeleteAccountView(APIView):
    def delete(self, request):
        user = request.user
        if user.is_authenticated:
            print('yiyi')
            user.delete()
            return Response({'message': 'Account deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            print('Not authenticated')
            return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)