"""Vista del auxiliar de sistemas."""

# Filtros
from django_filters.rest_framework import DjangoFilterBackend
# Django REST Framework
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
# Permisos
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from andromeda.modules.loans.models import Loans
from andromeda.modules.loans.serializers import LoansModelSerializer
from andromeda.modules.maintenance.models import Maintenance
from andromeda.modules.maintenance.serializers import MaintenanceModelSerializer
from andromeda.modules.technical_support.models import Support
from andromeda.modules.technical_support.serializers import SupportModelSerializer
# Modelos
from andromeda.roles.assistant.models import Assistant
# Serializers
from andromeda.roles.assistant.serializers import AssistantModelSerializer
from andromeda.users.models import User
from andromeda.users.permissions import IsAccountOwner
from andromeda.users.serializers import UserModelSerializer


class AssistantViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    """View set de los auxiliares de sistemas."""

    # Filtros
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('reputacion', 'availability')

    def get_queryset(self):
        """Regresa los usuarios con el rol de auxiliar de sistemas."""
        if self.action not in ['list']:
            return Assistant.objects.all()
        return User.objects.filter(is_assistant=True)

    def get_serializer_class(self):
        """Regresa el serializer basado en la accion."""
        if self.action == 'list':
            return UserModelSerializer
        return AssistantModelSerializer

    def get_permissions(self):
        """Asigna los permisos basados en la acción."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsAccountOwner)
        return [p() for p in permissions]

    @action(detail=False, methods=['get'])
    def services_stats(self, request, *args, **kwargs):
        """Muestra informacion relevante de prueba."""
        assistants = Assistant.objects.all().count()

        supports_completed = Support.objects.filter(
            status_support='Completado').count()

        loans_completed = Loans.objects.filter(
            status_loans='Completado').count()

        services_totals = Support.objects.all().count() + Loans.objects.all().count()
        services_pending = Support.objects.filter(is_active=True).count() + Loans.objects.filter(is_active=True).count()

        data = {
            'active_assistants': assistants,
            'services_totals': services_totals,
            'services_completed': supports_completed + loans_completed,
            'services_pending': services_pending,
            'supports': Support.objects.all().count(),
            'loans': Loans.objects.all().count(),
            'maintenances': Maintenance.objects.all().count(),
        }

        return Response(data)

    @action(detail=True, methods=['get'])
    def services_assigned(self, request, *args, **kwargs):
        """Servicios asignados al auxiliar."""
        support_assigned = Support.objects.filter(
            assigned_auxiliary=self.get_object()
        )
        loans_assigned = Loans.objects.filter(
            assigned_auxiliary=self.get_object()
        )

        maintenance_assigned = Maintenance.objects.filter(
            assigned_auxiliary=self.get_object()
        )

        data = {
            'supports_assigned': SupportModelSerializer(support_assigned, many=True).data,
            'loans_assigned': LoansModelSerializer(loans_assigned, many=True).data,
            'maintenance_assigned': MaintenanceModelSerializer(maintenance_assigned, many=True).data,
        }
        return Response(data)
