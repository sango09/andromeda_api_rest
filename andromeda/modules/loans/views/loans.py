"""Vista del modulo de prestamos."""

# Utilidades
import environ

# Django REST Framework
from rest_framework import mixins, viewsets

# Filtros
from rest_framework.filters import SearchFilter, OrderingFilter

# Permisos
from rest_framework.permissions import IsAuthenticated
from andromeda.modules.technical_support.permissions import (
    IsServiceOwner,
    IsPersonalAuthorized
)

# Modelos
from andromeda.modules.loans.models import Loans, InventoryLoans

# Serializers
from andromeda.modules.loans.serializers import (
    LoansModelSerializer,
    CreateLoansSerializer,
)
from andromeda.tasks.google_calendar import google_calendar_service

env = environ.Env()


class LoansViewSet(mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """View set del modulo de prestamos tecnologicos."""

    # Filtros de busqueda
    filter_backends = (SearchFilter, OrderingFilter)
    ordering = ('loans_date', 'complete_loans_date', 'assigned_auxiliary')
    ordering_fields = ('loans_date', 'complete_loans_date', 'assigned_auxiliary')
    search_fields = 'loans_location'

    queryset = Loans.objects.all()

    def perform_destroy(self, instance):
        """Cancela el servicio de soporte y elimina
        el evento programado en el calendario de Google Calendar."""

        instance.is_active = False
        instance.status_loans = 'Cancelado'

        # Eliminación del evento en el calendario
        google_calendar_service(
            calendar=env('CALENDAR_LOANS'),
            eventId=instance.event_google_id,
            calendarDelete=True
        )

        # Actualización de stock en el inventario de prestamos
        implement = InventoryLoans.objects.get(id=instance.implement.id)
        implement.implements_available += instance.ammount_implements
        implement.implements_used -= instance.ammount_implements
        implement.save()

        instance.save()

    def get_permissions(self):
        """Asigna los permisos basado en la acción."""
        permissions = [IsAuthenticated]
        if self.action in ['destroy']:
            permissions.append(IsServiceOwner)
        else:
            permissions.append(IsPersonalAuthorized)
        return [p() for p in permissions]

    def get_serializer_class(self):
        """Regresa el serializer basado en la acción."""
        if self.action == 'create':
            return CreateLoansSerializer
        return LoansModelSerializer
