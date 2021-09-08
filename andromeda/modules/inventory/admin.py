"""Admin de inventario."""

# Django
from django.contrib import admin

# Modelos
from andromeda.modules.inventory.models import Inventory, TechnicalDataSheet


@admin.register(TechnicalDataSheet)
class TechnicalDataSheetAdmin(admin.ModelAdmin):
    """Modelo del admin para las fichas tecnicas de los implementos."""
    list_display = ('id', 'picture',
                    'brand_implement', 'model_implement',
                    'operating_system', 'specifications',)
    search_fields = ('brand_implement', 'model_implement', 'operating_system')


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    """Modelo del admin para el inventario tecnologico."""
    list_display = ('serial_number', 'name',
                    'category', 'technical_data_sheet',
                    'purchase_date', 'price', 'assigned_user',
                    'status_implement')
    search_fields = ('category', 'assigned_user', 'status_implement')
