"""Admin de prestamos tecnologicos."""

# Django
from django.contrib import admin

# Modelos
from .models import Loans, InventoryLoans


@admin.register(Loans)
class LoansAdmin(admin.ModelAdmin):
    """Modelo del admin para los prestamos tecnologicos."""
    list_display = ('request_by', 'assigned_auxiliary',
                    'loans_location', 'loans_date',
                    'is_active', 'implement',
                    'ammount_implements'
                    )
    search_fields = ('request_by__user__email', 'assigned_auxiliary__user__email', 'implement__name')


@admin.register(InventoryLoans)
class InventoryLoansAdmin(admin.ModelAdmin):
    """Modelo del admin para el inventario de los prestamos tecnologicos."""
    list_display = ('implement', 'implements_available', 'implements_used', 'total_implements')
    list_filter = ('implement',)
