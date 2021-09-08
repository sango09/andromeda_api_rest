"""SetUp de los modulos"""

# Utilidades
import json

# Django REST Framework
import factory
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Modelos
from andromeda.modules.test_model.mocks import (
    UserEmployeeFactory,
    AssistantFactory,
    UserAdminFactory,
    InventoryFactory,
    InventoryLoansFactory,
    TechnicalDataSheetFactory,
)
from andromeda.roles.employee.models import Employee


class SupportSetUpAPIViewModel(APITestCase):
    """SetUp de prueba para modulo de soporte tecnico."""

    def setUp(self):
        # Usuario que solicita el soporte
        self.user = UserEmployeeFactory()
        Employee.objects.create(user=self.user)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        # Creacion de auxiliares
        AssistantFactory.create_batch(4)

        # Datos de creacion del soporte
        self.url = 'http://localhost:8000/api/support/'
        self.data = {
            'support_location': 'Teatro',
            'support_date': '2021-03-12 12:00:00',
            'description_problem': 'No tengo internet'

        }
        self.response = self.client.post(self.url, self.data)

        # Datos de actualizacion del soporte
        self.support_id = json.loads(self.response.content)
        self.support_url = '{}{}/'.format(self.url, self.support_id.get('id'))
        self.data_update = {
            'support_location': 'Salon 405 - Correcto'
        }

        self.complete_support_data = {
            'complete_support_date': '2021-03-12 16:00:00',
            'is_active': False
        }

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')


class MaintenanceSetUpAPIViewModel(APITestCase):
    """Setup de prueba para modulo de Mantenimiento."""

    def setUp(self):
        """Usuario que agenda el soporte"""
        self.user = UserAdminFactory()
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        # Creacion de auxiliares
        AssistantFactory.create_batch(4)

        # Creación de implemento
        self.implement = InventoryFactory()

        # Datos de mantenimiento
        self.url = 'http://localhost:8000/api/maintenance/'
        self.data = {
            'maintenance_location': 'ICT 2',
            'maintenance_date': '2021-03-24 11:00:00',
            'maintenance_type': 'Preventivo',
            'description': 'Mantenimiento preventivo a portatil HP de multitareas que tiene fallos de rendimiento',
            'implement': f'{self.implement.id}',
        }
        self.response = self.client.post(self.url, self.data)

        # Datos de actualización de mantenimiento
        self.response_content = json.loads(self.response.content)
        self.maintenance_url = '{}{}/'.format(self.url, self.response_content.get('id'))
        self.data_update = {
            'maintenance_location': 'ICT 1',
            'maintenance_date': '2021-03-24 15:00:00',
        }

        self.complete_maintenance_data = {
            'complete_maintenance_date': '2021-03-24 16:00:00',
            'is_active': False
        }

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')


class LoansSetUpAPIViewModel(APITestCase):
    """Setup de prueba para modulo de prestamos tecnologicos."""

    def setUp(self):
        """Usuario que solicitara el prestamos tecnologico"""
        self.user = UserEmployeeFactory()
        Employee.objects.create(user=self.user)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        # Creación de auxiliares
        AssistantFactory.create_batch(4)

        # Creación de implementos para prestamo
        self.implement = InventoryLoansFactory()

        # Datos de prestamo
        self.url = 'http://localhost:8000/api/loans/'
        self.data = {
            'loans_location': 'Admisiones',
            'loans_date': '2021-03-24 10:30:00',
            'implement': f'{self.implement.id}',
            'ammount_implements': '10',
            'comments': 'Necesito los 10 equipos completamente cargados'
        }
        self.response = self.client.post(self.url, self.data)

        # Datos de actualización del prestamo
        self.response_content = json.loads(self.response.content)
        self.loans_url = '{}{}/'.format(self.url, self.response_content.get('id'))
        self.data_update = {
            'loans_location': 'Salon 405',
            'loans_date': '2021-03-24 12:30:00',
        }

        self.complete_loans_data = {
            'complete_loans_date': '2021-03-24 12:00:00',
            'is_active': False
        }

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')


class InventorySetUpAPIViewModel(APITestCase):
    """Setup de prueba para modulo de Inventario."""

    def setUp(self):
        """Administrador que agrega los implementos al inventario."""
        self.user = UserAdminFactory()
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        # Creación de fichas tecnicas.
        self.tech_tab = TechnicalDataSheetFactory()

        # Datos de implemento
        self.url = 'http://localhost:8080/api/inventory/'
        self.data = {
            'name': 'Macbook Pro',
            'category': 'Portatil',
            'serial_number': factory.Faker('md5', raw_output=False),
            'purchase_date': '2021-03-21',
            'price': '0.000.000',
            'status_implement': 'Nuevo Ingreso',
            'technical_data_sheet': f'{self.tech_tab.id}',
        }
        self.response = self.client.post(self.url, self.data)

        # Datos de actualización de implemento
        self.response_content = json.loads(self.response.content)
        self.implement_url = '{}{}/'.format(self.url, self.response_content.get('id'))
        self.new_tech_tab = TechnicalDataSheetFactory()
        self.data_update = {
            'status_implement': 'Inhabilitado',
            'technical_data_sheet_id': f'{self.new_tech_tab.id}',
        }

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
