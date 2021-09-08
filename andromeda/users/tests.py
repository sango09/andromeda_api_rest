"""Test de usuarios"""

# Utilidades
import json

# Django
from rest_framework import status

# Django REST Framework
from rest_framework.test import APITestCase

# Modelos
from andromeda.users.models import User


class UserRegistrationAPIViewTestCase(APITestCase):
    """Caso de prueba del registro de usuarios"""
    url = 'http://localhost:8000/api/users/signup/'

    def test_invalid_password(self):
        """Valida que las contraseñas sean correctas"""
        user_data = {
            'first_name': 'Pedro',
            'last_name': 'Gomez',
            'email': 'test_model@testuser.com',
            'username': 'test_model@testuser.com',
            'password': 'password',
            'password_confirmation': 'INVALID_PASSWORD',
            'is_admin': True,
        }

        response = self.client.post(self.url, user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration(self):
        """Prueba que los datos de registros sean almacenados"""
        user_data_1 = {
            'first_name': 'Pedro',
            'last_name': 'Gomez',
            'email': 'test_model@tesuser.com',
            'username': 'test_model@tesuser.com',
            'password': 'G@mez123456',
            'password_confirmation': 'G@mez123456',
            'is_admin': True,
        }

        response = self.client.post(self.url, user_data_1, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("profile" in json.loads(response.content))


class UserLoginAPIViewTestCase(APITestCase):
    """Caso de prueba para autenticacion de credenciales de ingreso"""
    url = 'http://localhost:8000/api/users/login/'

    def setUp(self):
        self.username = 'john'
        self.email = 'john@gmail.com'
        self.password = 'you_know_nothing'
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_authentication_without_password(self):
        response = self.client.post(self.url, {'email': 'santiagofl123@gmail.com'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authentication_with_wrong_password(self):
        response = self.client.post(self.url, {'email': self.email, 'password': 'you_know_my_password'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authentication_with_valid_data(self):
        response = self.client.post(self.url, {'email': self.email, 'password': self.password})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('access_token' in json.loads(response.content))
