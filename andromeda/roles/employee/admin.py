"""Admin de empleados"""

# Django
from django.contrib import admin

# Modelos
from andromeda.roles.employee.models import Employee


@admin.register(Employee)
class AssistantAdmin(admin.ModelAdmin):
    """Modelo del admin empleados"""
    list_display = ('user', 'work_area', 'position', 'technical_support_request', 'is_active')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
