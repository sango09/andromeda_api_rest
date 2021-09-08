"""Vista del inventario del modulo de prestamos tecnologicos."""

# Django REST Framework
from rest_framework import viewsets, mixins

# Permisos
from rest_framework.permissions import IsAuthenticated
from andromeda.modules.inventory.permissions import IsAdmin, IsStaff

# Modelos
from andromeda.modules.loans.models import InventoryLoans
# Serializers
from andromeda.modules.loans.serializers import InventoryLoansSerializer, CreateInventoryLoansSerializer


class InventoryLoansViewSet(mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    """View set del inventario para el modulo de prestamos tecnologicos."""

    queryset = InventoryLoans.objects.all()

    def get_permissions(self):
        """Asigna los permisos basados en la acción."""
        permissions = [IsAuthenticated]
        if self.action in ['destroy']:
            permissions.append(IsAdmin)
        elif self.action in ['update', 'partial_update']:
            permissions.append(IsStaff)
        return (p() for p in permissions)

    def get_serializer_class(self):
        """Asigna el serializer basado en la acción."""
        if self.action == 'create':
            return CreateInventoryLoansSerializer
        return InventoryLoansSerializer
