"""Admin del auxiliar de sistemas."""

# Django
from django.contrib import admin

# Modelos
from andromeda.roles.assistant.models import Assistant


@admin.register(Assistant)
class AssistantAdmin(admin.ModelAdmin):
    """Modelo del admin de perfiles de usuarios."""
    list_display = ('user', 'availability', 'reputation', 'is_active')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
