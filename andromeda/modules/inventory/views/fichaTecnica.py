"""Vista de ficha tecnica."""

# Django rest
from rest_framework import mixins, viewsets
# Permisos
from rest_framework.permissions import IsAuthenticated
from andromeda.modules.inventory.permissions import IsAdmin, IsStaff

# Modelos
from andromeda.modules.inventory.models import TechnicalDataSheet

# Serializer
from andromeda.modules.inventory.serializers import TechnicalDataSheetModelSerializer


class FichaTecnicaViewSet(mixins.RetrieveModelMixin,
                          mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """View set de fichaTecnica."""

    serializer_class = TechnicalDataSheetModelSerializer
    queryset = TechnicalDataSheet.objects.all()

    def get_permissions(self):
        """Asigna los permisos basado en la acción."""
        permissions = [IsAuthenticated]
        if self.action in ['destroy']:
            permissions.append(IsAdmin)
        else:
            permissions.append(IsStaff)
        return [p() for p in permissions]
