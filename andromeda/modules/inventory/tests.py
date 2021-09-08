"""Test del modulo de inventario"""

# Utilidades
import json

# Django REST Framework
from rest_framework import status
from rest_framework.authtoken.models import Token

# Modelos
from andromeda.modules.inventory.models import Inventory
# Mocks
from andromeda.modules.test_model.mocks import (
    UserAssistantFactory,
    UserEmployeeFactory,
)
# SetUp Model
from andromeda.modules.test_model.setUp_modules import InventorySetUpAPIViewModel


class InventoryCreateAPIViewTestCase(InventorySetUpAPIViewModel):
    """Caso de prueba de agregar implemento al inventario"""

    def test_techtab_generation(self):
        """Verifica que la ficha tecnica fue generada exitosamente"""
        response = self.client.get(f'http://localhost:8080/api/tech-tab/{self.tech_tab.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_implement(self):
        """Implemento agregado exitosamente"""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


class InventoryAuthorizationAPIViewTestCase(InventorySetUpAPIViewModel):
    """Caso de prueba de autorización de roles"""

    def test_authorization_with_employee(self):
        """Prueba de autorización con el rol de empleado"""
        new_user = UserEmployeeFactory()
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {new_token.key}')

        # HTTP GET
        response = self.client.get(self.implement_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # HTTP POST
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # HTTP PUT
        response = self.client.put(self.implement_url, self.data_update)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # HTTO PATCH
        response = self.client.patch(self.implement_url, self.data_update)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # HTTP DELETE
        response = self.client.delete(self.implement_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorization_with_assistant(self):
        """Prueba de authorization con el rol de auxiliar de sistemas"""
        new_user = UserAssistantFactory()
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {new_token.key}')

        # HTTP GET
        response = self.client.get(self.implement_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # HTTP POST
        new_data = self.data.copy()
        new_data['serial_number'] = 'Sdx45687951312'
        response = self.client.post(self.url, new_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # HTTO PATCH
        response = self.client.patch(self.implement_url, self.data_update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # HTTP DELETE
        response = self.client.delete(self.implement_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class InventoryDetailAPIViewTestCase(InventorySetUpAPIViewModel):
    """Caso de prueba del implemento creado"""

    def test_implement_object_update(self):
        """Prueba de actualziación de datos del implemento"""
        response = self.client.patch(self.implement_url, self.data_update)
        response_data = json.loads(response.content)

        implement = Inventory.objects.get(id=self.response_content.get('id'))
        self.assertEqual(implement.technical_data_sheet.id, response_data['technical_data_sheet']['id'])
        self.assertEqual(implement.status_implement, response_data.get('status_implement'))

    def test_implement_object_delete(self):
        """Prueba de inhabilitar implemento"""
        response = self.client.delete(self.implement_url)
        implement = Inventory.objects.get(id=self.response_content.get('id'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(implement.status_implement, 'Inactivo')
