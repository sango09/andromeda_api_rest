"""Test del modulo de soporte tennico."""

# Utilidades
import json

# Django REST Framework
from rest_framework import status
from rest_framework.authtoken.models import Token

# Modelos
from andromeda.modules.technical_support.models import Support
from andromeda.roles.assistant.models import Assistant

# Mocks
from andromeda.modules.test_model.mocks import UserEmployeeFactory

# SetUp Model
from andromeda.modules.test_model.setUp_modules import SupportSetUpAPIViewModel


class SupportCreateAPIViewTestCase(SupportSetUpAPIViewModel):
    """Caso de prueba de crear un soporte tecnico."""

    def test_create_support(self):
        """Soporte tecnico exitoso."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


class SupportDetailAPIViewTestCase(SupportSetUpAPIViewModel):
    """Caso de prueba de los detalles del soporte solicitado."""

    def test_support_object_bundle(self):
        """Verifica la creación del soporte."""
        response = self.client.get(self.support_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_support_object_support_authorization(self):
        """Prueba de actualización con token distinto."""
        new_user = UserEmployeeFactory()
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {new_token.key}')

        # HTTP PUT
        response = self.client.put(self.support_url, self.data_update)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # HTTP PATCH
        response = self.client.patch(self.support_url, self.data_update)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # HTTP DELETE
        response = self.client.delete(self.support_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_support_object_update(self):
        """Prueba de actualización con token valido."""
        response = self.client.patch(self.support_url, self.data_update)
        response_data = json.loads(response.content)
        support = Support.objects.get(id=self.support_id.get('id'))
        self.assertEqual(response_data.get('support_location'), support.support_location)

    def test_support_object_complete(self):
        """Prueba de completar el soporte tecnico."""
        response = self.client.patch(self.support_url, self.complete_support_data)

        # Obtener datos de response
        response_data = json.loads(response.content)
        employee_support_count = response_data['request_by']['employee']['technical_support_request']
        assistant = Assistant.objects.get(id=response_data.get('auxiliary_id'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(employee_support_count, 1)
        self.assertEqual(assistant.technical_support_completed, 1)

    def test_support_object_rating(self):
        """Prueba de calificar el soporte tecnico completado"""

        data_rate = {
            'rating': '5.0',
            'comments': 'Fue muy amable'
        }
        response = self.client.post(f'{self.support_url}rate/', data_rate)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data.get('rating'), float(data_rate.get('rating')))

    def test_support_object_delete(self):
        """Prueba de cancelar el soporte tecnico"""
        response = self.client.delete(self.support_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
