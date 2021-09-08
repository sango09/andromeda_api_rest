"""App de mantenimientos."""

# Django
from django.apps import AppConfig


class MaintenanceAppConfig(AppConfig):
    """Config del app de mantenimiento."""
    name = 'andromeda.modules.maintenance'
    verbose_name = 'Maintenance'
