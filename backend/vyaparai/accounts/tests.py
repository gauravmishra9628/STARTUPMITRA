from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class AuthApiTests(APITestCase):
    def test_register_login_and_profile(self):
        register_payload = {
            'username': 'founder1',
            'email': 'founder1@example.com',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!',
            'first_name': 'Founder',
            'last_name': 'One',
            'language': 'en',
        }

        register_response = self.client.post('/api/auth/register/', register_payload, format='json')
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', register_response.data)
        self.assertIn('refresh', register_response.data)

        login_response = self.client.post(
            '/api/auth/login/',
            {'email': register_payload['email'], 'password': register_payload['password']},
            format='json',
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        profile_response = self.client.get('/api/auth/profile/')
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data['email'], register_payload['email'])
