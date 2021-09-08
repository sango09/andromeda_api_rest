"""Vista del modulo de mantenimiento."""

# Utilidades
import environ

# Django REST Framework
from rest_framework import mixins, viewsets

# Filtros
from rest_framework.filters import SearchFilter, OrderingFilter

# Permisos
from rest_framework.permissions import IsAuthenticated
from andromeda.modules.inventory.permissions import IsAdmin, IsStaff

# Modelos
from andromeda.modules.maintenance.models import Maintenance
from andromeda.modules.inventory.models import Inventory

# Serializers
from andromeda.modules.maintenance.serializers import (
    MaintenanceModelSerializer,
    CreateMaintenanceSerializer,
)
# Tareas
from andromeda.tasks.google_calendar import google_calendar_service

env = environ.Env()


class MaintenanceViewSet(mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """View set del modulo de mantenimientos."""

    # Filtros de busqueda
    filter_backends = (SearchFilter, OrderingFilter)
    ordering = ('maintenance_date', 'complete_maintenance_date', 'assigned_auxiliary')
    ordering_fields = ('maintenance_date', 'complete_maintenance_date', 'assigned_auxiliary')
    search_fields = 'maintenance_location'
    queryset = Maintenance.objects.all()

    def perform_destroy(self, instance):
        """Cambia el estado del mantenimiento a inactivo ,actualiza el estado del implemento
        y elimina el evento del calendario de Google Calendar."""

        instance.is_active = False
        instance.status_maintenance = 'Cancelado'

        # Elimina el evento
        google_calendar_service(
            calendar=env('CALENDAR_MAINTENANCES'),
            eventId=instance.event_google_id,
            calendarDelete=True,
        )

        # Actualiza el estado
        implement = Inventory.objects.get(pk=instance.implement_id)
        implement.status_implement = 'Pendiente de mantenimiento'
        implement.save()

        instance.save()

    def get_permissions(self):
        """Asigna los permisos basados en la acción."""
        permissions = [IsAuthenticated]
        if self.action in ['destroy']:
            permissions.append(IsAdmin)
        else:
            permissions.append(IsStaff)
        return [p() for p in permissions]

    def get_serializer_class(self):
        """Regresa el serializer basado en la acción."""
        if self.action == 'create':
            return CreateMaintenanceSerializer

        return MaintenanceModelSerializer
