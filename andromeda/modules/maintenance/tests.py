"""Test del modulo de mantenimientos."""

# Utilidades
import json
from datetime import datetime

# Django REST Framework
from rest_framework import status
from rest_framework.authtoken.models import Token

# Modelos
from andromeda.modules.inventory.models import Inventory
from andromeda.modules.maintenance.models import Maintenance
from andromeda.roles.assistant.models import Assistant

# Mocks
from andromeda.modules.test_model.mocks import (
    UserAssistantFactory,
    UserEmployeeFactory,
)
# SetUp Model
from andromeda.modules.test_model.setUp_modules import MaintenanceSetUpAPIViewModel


class MaintenanceCreateAPIViewTestCase(MaintenanceSetUpAPIViewModel):
    """Caso de prueba de agendar mantenimiento."""

    def test_create_maintenance(self):
        """Mantenimiento agendado exitosamente."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


class MaintenanceDetailAPIViewTestCase(MaintenanceSetUpAPIViewModel):
    """Caso de prueba de los detalles del mantenimiento."""

    def test_maintenance_object_bundle(self):
        """Verifica la creación del mantenimiento."""
        response = self.client.get(self.maintenance_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_maintenance_object_authorization_role(self):
        """Prueba de agendar mantenimiento con rol de empleado."""
        new_user = UserEmployeeFactory()
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {new_token.key}')

        # HTTP POST
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # HTTP PUT
        response = self.client.put(self.maintenance_url, self.data_update)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # HTTO PATCH
        response = self.client.patch(self.maintenance_url, self.data_update)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # HTTP DELETE
        response = self.client.delete(self.maintenance_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_maintenance_object_update(self):
        """Prueba de actualización con rol correcto y token valido."""
        response = self.client.patch(self.maintenance_url, self.data_update)
        response_data = json.loads(response.content)
        maintenance = Maintenance.objects.get(id=self.response_content.get('id'))

        format_date = '%Y-%m-%d %H:%M:%S'
        maintenance_new_date = maintenance.maintenance_date.strftime(format_date)
        maintenance_update_date = response_data.get('maintenance_date')
        maintenance_update_date = datetime.strptime(
            maintenance_new_date, format_date
        ).strftime(format_date)

        self.assertEqual(maintenance_update_date, maintenance_new_date)
        self.assertEqual(response_data.get('maintenance_location'), maintenance.maintenance_location)

    def test_maintenance_object_complete_assistant(self):
        """Prueba de mantenimiento completado por auxiliar
            antes de la fecha de solicitudes.
        """
        new_user = UserAssistantFactory()
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {new_token.key}')

        response = self.client.patch(self.maintenance_url, self.complete_maintenance_data)

        new_complete_data = {
            'complete_maintenance_date': '2021-03-24 10:00:00',
            'is_active': False
        }
        new_response = self.client.patch(self.maintenance_url, new_complete_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_maintenance_object_complete(self):
        """Prueba de mantenimiento completado."""

        # Datos de response
        response = self.client.patch(self.maintenance_url, self.complete_maintenance_data)
        response_data = json.loads(response.content)

        assistant = Assistant.objects.get(id=response_data.get('auxiliary_id'))
        implement = Inventory.objects.get(id=response_data['implement']['id'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(implement.status_implement, 'Disponible')
        self.assertEqual(assistant.maintenance_completed, 1)

    def test_maintenance_object_delete(self):
        """Prueba de cancelar el mantenimiento"""
        response = self.client.delete(self.maintenance_url)
        import pdb; pdb.set_trace()
        implement = Inventory.objects.get(id=self.response_content['implement'])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(implement.status_implement, 'Pendiente de mantenimiento')
