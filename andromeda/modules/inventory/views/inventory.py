"""Vista del modulo de inventario."""

# Django REST Framework
from rest_framework import mixins, viewsets

# Permisos
from rest_framework.permissions import IsAuthenticated
from andromeda.modules.inventory.permissions import IsAdmin, IsStaff

# Modelos
from andromeda.modules.inventory.models import Inventory

# Serializers
from andromeda.modules.inventory.serializers import (
    InventorySerializer,
    IngresarImplementoSerializer
)


class InventoryViewSet(mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    """View set de inventario."""

    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()

    def get_permissions(self):
        """Asigna los permisos basado en la acción."""
        permissions = [IsAuthenticated]
        if self.action in ['destroy']:
            permissions.append(IsAdmin)
        else:
            permissions.append(IsStaff)
        return [p() for p in permissions]

    def perform_destroy(self, instance):
        """Inactiva el implemento."""
        instance.status_implement = 'Inactivo'
        instance.save()

    def get_serializer_class(self):
        """Asigna el serializer segun la acción."""
        if self.action == 'create':
            return IngresarImplementoSerializer
        return InventorySerializer
