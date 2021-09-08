"""Test del modulo de prestamos tecnologicos"""

# Utilidades
import json

# Django REST Framework
from rest_framework import status
from rest_framework.authtoken.models import Token

# Modelos
from andromeda.modules.loans.models import (
    InventoryLoans,
    Loans,
)
from andromeda.roles.assistant.models import Assistant
from andromeda.roles.employee.models import Employee
# Mocks
from andromeda.modules.test_model.mocks import (
    UserEmployeeFactory,
    AssistantFactory,
)
# SetUp Model
from andromeda.modules.test_model.setUp_modules import LoansSetUpAPIViewModel


class LoansCreateAPIViewTestCase(LoansSetUpAPIViewModel):
    """Caso de prueba de agendar prestamo"""

    def test_create_loans(self):
        """Prestamo agendado con distintas horas"""

        # Prestamo agendado con 2 horas de anticipación
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

        # Prestamo agendado con menos de 2 horas de anticipación
        new_data = self.data.copy()
        new_data['loans_date'] = '2021-03-21 21:30:00'
        response = self.client.post(self.url, new_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_implement_quantity_request(self):
        """Prueba de cantidad de implementos disponibles"""

        # Prestamo con 101 implementos solicitados
        new_data = self.data.copy()
        new_data['ammount_implements'] = '101'
        response = self.client.post(self.url, new_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_implements_used_loans(self):
        """Prueba de cantidad de implementos
        apartados en el inventario de prestamos."""

        # Implementos solicitados
        response_data = json.loads(self.response.content)
        implement = InventoryLoans.objects.get(id=response_data.get('implement'))
        self.assertEqual(implement.implements_used, response_data.get('ammount_implements'))

        # Verifica que los implementos solicitados sean restados de los disponibles
        implements_available = implement.total_implements - implement.implements_used
        self.assertEqual(implement.implements_available, implements_available)


class LoansDetailAPIViewTestCase(LoansSetUpAPIViewModel):
    """Caso de prueba de los detalles del prestamo
    con las credenciales del usuario que solicito el prestamo"""

    def test_loans_object_bundle(self):
        """Verifica la creación del prestamo"""
        response = self.client.get(self.loans_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_loans_object_update(self):
        """Prueba de actualización de prestamo"""
        response = self.client.patch(self.loans_url, self.data_update)
        response_data = json.loads(response.content)
        loans = Loans.objects.get(id=self.response_content.get('id'))
        self.assertEqual(response_data.get('loans_location'), loans.loans_location)

    def test_loans_object_delete(self):
        """Prueba de cancelar el prestamo"""
        response = self.client.delete(self.loans_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LoansAuthorizationAPiViewTestCase(LoansSetUpAPIViewModel):
    """Caso de prueba de permisos de usuario segun su rol."""

    def test_loans_object_authorization(self):
        """Prueba de autorización con distintos usuarios"""

        # Usuario distinto al que agendo el prestamo
        new_user = UserEmployeeFactory()
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {new_token.key}')

        # HTTP PUT
        response = self.client.put(self.loans_url, self.data_update)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # HTTP PATCH
        response = self.client.patch(self.loans_url, self.data_update)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # HTTP DELETE
        response = self.client.delete(self.loans_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_loans_object_completed(self):
        # Usuario con rol de auxiliar de sistemas
        assistant = AssistantFactory()
        new_token = Token.objects.create(user=assistant.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {new_token.key}')

        # Completar prestamo 1 hora antes de haber sido agendado el prestamo
        new_data_update = self.complete_loans_data.copy()
        new_data_update['complete_loans_date'] = '2021-03-24 11:00:00'
        response = self.client.patch(self.loans_url, new_data_update)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Completar prestamo 1 hora despues del prestamo
        response = self.client.patch(self.loans_url, self.complete_loans_data)
        response_content = json.loads(response.content)
        assistant = Assistant.objects.get(id=self.response_content.get('auxiliary_id'))
        request_by_employee = Employee.objects.get(user=response_content['request_by']['id'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(assistant.loans_completed, 1)
        self.assertEqual(request_by_employee.loans_request, 1)

        # Cancelar prestamo
        response = self.client.delete(self.loans_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
