from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError

class RegisterView(APIView):
    def post(self, request):
        data = request.data

        # Extract and validate fields
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
            validate_password(password1)  # Use Django's built-in password validators
        except ValidationError as e:
            return Response({'errors': {'password': e.messages}}, status=status.HTTP_400_BAD_REQUEST)

        # Check for unique username and email
        if User.objects.filter(username=username).exists():
            return Response({'errors': {'username': 'Username already exists.'}}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'errors': {'email': 'Email already exists.'}}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password1)
        return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)



    


