"""App de inventario."""

# Django
from django.apps import AppConfig


class InventoryAppConfig(AppConfig):
    """Config del app de inventario."""
    name = 'andromeda.modules.inventory'
    verbose_name = 'Inventory'
