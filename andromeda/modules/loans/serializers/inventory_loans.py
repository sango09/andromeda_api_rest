"""Serializer del inventario de prestamos tecnologicos."""

# Django REST Framework
from rest_framework import serializers

# Serializer
from andromeda.modules.inventory.serializers import InventorySerializer

# Modelos
from andromeda.modules.loans.models import InventoryLoans


class InventoryLoansSerializer(serializers.ModelSerializer):
    """Serializer para el inventario de los prestamos tecnologicos."""

    implement = InventorySerializer(read_only=True)

    class Meta:
        """Clase Meta."""
        model = InventoryLoans
        fields = '__all__'
        read_only_fields = (
            'total_implements',
            'last_admission'
        )


class CreateInventoryLoansSerializer(serializers.ModelSerializer):
    """Serializer para agregar implementos al inventario
    del modulo de prestamos tecnologicos."""

    class Meta:
        """Clase Meta."""
        model = InventoryLoans
        exclude = ('implements_used', 'total_implements')

    def create(self, data):
        """Agrega el implemento al inventario de prestamos tecnologicos."""
        implement = InventoryLoans.objects.create(**data, total_implements=data['implements_available'])
        return implement
