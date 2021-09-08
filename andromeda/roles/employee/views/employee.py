"""Vista de empleado"""

# Filtros
from django.db.models.aggregates import Sum
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
from andromeda.modules.technical_support.models import Support
from andromeda.modules.technical_support.serializers import SupportModelSerializer
# Modelos
from andromeda.roles.employee.models import Employee
# Serializers
from andromeda.roles.employee.serializers import EmployeeModelSerializer
from andromeda.users.permissions import IsAccountOwner


class EmployeeViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    """View set para el rol de empleado"""

    serializer_class = EmployeeModelSerializer

    # Filtros
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('technical_support_request', 'loans_request')
    queryset = Employee.objects.all()

    def get_permissions(self):
        """Asigna los permisos basados en la acción"""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsAccountOwner)
        return [p() for p in permissions]

    @action(detail=True, methods=['get'])
    def request_services(self, request, *args, **kwargs):
        """Servicios solicitados por el empleado"""
        support_request = Support.objects.filter(
            request_by=self.get_object().user
        )
        loans_request = Loans.objects.filter(
            request_by=self.get_object().user
        )

        data = {
            'support_request': SupportModelSerializer(support_request, many=True).data,
            'loans_request': LoansModelSerializer(loans_request, many=True).data,
        }

        return Response(data)

    @action(detail=True, methods=['get'])
    def stats(self, request, *args, **kwargs):
        """Información de empleado"""
        implements_request = Loans.objects.filter(
            request_by=self.get_object().user
        ).aggregate(
            Sum('ammount_implements')
        )
        supports_completed = Support.objects.filter(
            request_by=self.get_object().user,
            status_support='Completado'
        ).count()

        loans_completed = Loans.objects.filter(
            request_by=self.get_object().user,
            status_loans='Completado'
        ).count()

        data = {
            'supports_request': self.get_object().technical_support_request,
            'loans_request': self.get_object().loans_request,
            'implements_used': implements_request['ammount_implements__sum'],
            'supports_completed': supports_completed,
            'loans_completed': loans_completed,
        }
        return Response(data)
