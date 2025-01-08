from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch
from rest_framework.test import APIRequestFactory, force_authenticate
from user_service_app.views import ChangePasswordView, DeleteAccountView
from rest_framework.response import Response

class TestUserRegistration(TestCase):
    def test_register_user_OK_response(self):
        response = self.client.post('http://localhost:8002/register/',{
                'username': 'testuser',
                'email': 'samthe-1@student.ltu.se',
                'first_name':'test_first_name',
                'last_name': 'test_last_name',
                'password1': 'SuperSecurePassword123!',
                'password2': 'SuperSecurePassword123!',
            })
    
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_user_BAD_response(self):
        response = self.client.post('http://localhost:8002/register/',{
                'username': 'testuser',
                'email': 'samthe-1',
                'first_name':'test_first_name',
                'last_name': 'test_last_name',
                'password1': 'badpass',
                'password2': 'badpass!',
            })
    
        self.assertNotEqual(response.status_code, 201)
        self.assertFalse(User.objects.filter(username='testuser').exists())

class TestUserDeletion(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='SuperSecurePassword123!')
        self.factory = APIRequestFactory()

    @patch('user_service_app.views.DeleteAccountView.delete')
    def test_user_deletion_logged_in(self, mock_delete):
        mock_delete.return_value = Response({'message': 'Account deleted successfully.'}, status=204)

        request = self.factory.delete('/delete-account/')
        request.user = self.user

        response = DeleteAccountView.as_view()(request)
        self.assertEqual(response.status_code, 204)

    def test_user_deletion_not_logged_in(self):
        request = self.factory.delete('/delete-account/')

        response = DeleteAccountView.as_view()(request)
        self.assertEqual(response.status_code, 401)

class TestChangePasswordView(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', password='OldPassword123!')

    def test_valid_password_change(self):
        request = self.factory.post('/change-password/', {
            'current_password': 'OldPassword123!',
            'new_password1': 'NewSecurePassword123!',
            'new_password2': 'NewSecurePassword123!',
        })

        force_authenticate(request, user=self.user)

        response = ChangePasswordView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Password updated successfully.')

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewSecurePassword123!'))

    def test_invalid_password_change(self):
        request = self.factory.post('/change-password/', {
            'current_password': 'OtherPassword123!',
            'new_password1': 'NewSecurePassword123!',
            'new_password2': 'NewSecurePassword123!',
        })

        force_authenticate(request, user=self.user)

        response = ChangePasswordView.as_view()(request)

        self.assertEqual(response.status_code, 400)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('OldPassword123!'))