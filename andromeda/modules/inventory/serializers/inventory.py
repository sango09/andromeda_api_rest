"""Serializer del inventario de prestamos tecnologicos."""

# Django REST Framework
from rest_framework import serializers

# Modelos
from andromeda.modules.inventory.models import Inventory, TechnicalDataSheet
from andromeda.users.models import User
# Serializers
from andromeda.users.serializers import UserModelSerializer
from .technical_data_sheet import TechnicalDataSheetModelSerializer


class InventorySerializer(serializers.ModelSerializer):
    """Serializer para el inventario tecnologico."""

    technical_data_sheet = TechnicalDataSheetModelSerializer(read_only=True)
    assigned_user = UserModelSerializer(read_only=True)

    # Campos para actualizar datos
    technical_data_sheet_id = serializers.IntegerField(required=False)
    assigned_user_id = serializers.IntegerField(required=False)

    class Meta:
        """Clase Meta."""
        model = Inventory
        fields = '__all__'
        fields_read_only = (
            'technical_data_sheet',
            'serial_number',
            'purchase_date',
            'price',
            'assigned_user'
        )

    def update(self, instance, validated_data):
        """Actualiza los datos del inventario."""
        technical_data_sheet_id = validated_data.get('technical_data_sheet_id', None)
        assigned_user_id = validated_data.get('assigned_user_id', None)
        if technical_data_sheet_id is not None:
            instance.technical_data_sheet = TechnicalDataSheet.objects.get(id=technical_data_sheet_id)
        elif assigned_user_id is not None:
            instance.assigned_user = User.objects.get(id=assigned_user_id)
        instance.save()
        return super(InventorySerializer, self).update(instance, validated_data)


class IngresarImplementoSerializer(serializers.ModelSerializer):
    """Serializer para el ingreso de implementos."""

    class Meta:
        model = Inventory
        exclude = (
            'assigned_user',
        )
