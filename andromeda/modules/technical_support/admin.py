"""Admin de soporte tecnico."""

# Django
from django.contrib import admin

# Modelos
from .models import Support


@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    """Modelo del admin para el modulo de soporte tecnico."""
    list_display = ('request_by', 'assigned_auxiliary',
                    'support_location', 'support_date',
                    'rating', 'is_active')
    list_filter = ('is_active', 'support_location', 'assigned_auxiliary')
