"""Factory data"""

# Factory boy
import factory
from factory.django import DjangoModelFactory

# Modelos
from andromeda.modules.inventory.models import TechnicalDataSheet, Inventory
from andromeda.roles.assistant.models import Assistant
from andromeda.users.models import User
from andromeda.modules.loans.models import InventoryLoans


class UserFactory(DjangoModelFactory):
    """Modelo de factory boy para usuarios"""

    class Meta:
        """Clase Meta"""
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('safe_email')
    username = email
    password = 'you_know_nothing'


class UserAdminFactory(UserFactory):
    """Modelo de factory boy de usuario que hereda de UserFactory
    y le asigna el rol de administrador."""
    is_admin = True


class UserEmployeeFactory(UserFactory):
    """Modelo de factory boy de usuario que hereda de UserFactory
    y le asigna el rol de empleado."""
    is_employee = True


class UserAssistantFactory(UserFactory):
    """Modelo de factory boy de usuario que hereda de UserFactory
    y le asigna el rol de auxiliar de sistemas."""
    is_assistant = True


class AssistantFactory(DjangoModelFactory):
    """Modelo de factory boy de auxiliares de sistemas
    que tiene como instancia de usuario a UserAssistantFactory."""

    class Meta:
        """Clase Meta"""
        model = Assistant

    user = factory.SubFactory(UserAssistantFactory)


class TechnicalDataSheetFactory(DjangoModelFactory):
    """Modelo de factory boy para fichas tecnias con datos falsos."""

    class Meta:
        """Clase Meta"""
        model = TechnicalDataSheet

    brand_implement = factory.Faker('company')
    model_implement = factory.Faker('license_plate')
    operating_system = 'Windows 10'
    specifications = factory.Faker('numerify', text='Intel Core i%-%%##K vs AMD Ryzen % %%##X')


class InventoryFactory(DjangoModelFactory):
    """Modelo de factory boy de inventario que tiene
    como instancia de technical_data_sheet a TechnicalDataSheetFactory."""

    class Meta:
        """Clase Meta"""
        model = Inventory

    name = 'Equipo de prueba'
    category = 'prueba'
    technical_data_sheet = factory.SubFactory(TechnicalDataSheetFactory)
    serial_number = factory.Faker('md5', raw_output=False)
    purchase_date = factory.Faker('date')
    price = '0.000.000'
    status_implement = factory.Faker('word', ext_word_list=['Disponible',
                                                            'En mantenimiento',
                                                            'Nuevo ingreso',
                                                            'No disponible'])


class InventoryLoansFactory(DjangoModelFactory):
    """Modelo de factory boy de inventario de prestamos tecnologicos
    tiene como instancia de implement a InventoryFactory"""

    class Meta:
        """Clase Meta"""
        model = InventoryLoans

    implement = factory.SubFactory(InventoryFactory)
    implements_available = '100'
    implements_used = '0'
    total_implements = '100'
