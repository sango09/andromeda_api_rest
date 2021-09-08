"""Serializer de la ficha tecnica de un implemento tecnologico."""

# Django REST Framework
from rest_framework import serializers

# Modelos
from andromeda.modules.inventory.models import TechnicalDataSheet


class TechnicalDataSheetModelSerializer(serializers.ModelSerializer):
    """Serializer base de ficha tecnica."""

    class Meta:
        """Clase Meta"""
        model = TechnicalDataSheet
        fields = '__all__'


class IngresarFichaTecnica(serializers.ModelSerializer):
    """Serializer para el ingreso de fichas tecnicas."""

    class Meta:
        model = TechnicalDataSheet
        fields = (
            'id',
            'picture',
            'brand_implement',
            'model_implement',
            'operating_system',
            'specifications'
        )
