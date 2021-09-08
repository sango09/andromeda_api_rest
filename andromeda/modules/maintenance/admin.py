"""Admin de mantenimientos."""

# Django
from django.contrib import admin

# Modelos
from .models import Maintenance


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    """Modelo del admin para el modulo de mantenimientos."""
    list_display = ('request_by', 'assigned_auxiliary',
                    'maintenance_location', 'maintenance_date',
                    'maintenance_type', 'implement',
                    'is_active')

    search_fields = ('request_by__user__email', 'assigned_auxiliary__user__email', 'implement__name')
