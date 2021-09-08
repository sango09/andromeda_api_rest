"""Serializer de los auxiliares de sistemas."""

# Django REST Framework
from rest_framework import serializers

# Modelos
from andromeda.roles.assistant.models import Assistant


class AssistantModelSerializer(serializers.ModelSerializer):
    """Serializer del rol de auxiliar de sistemas."""

    class Meta:
        """Clase Meta."""
        model = Assistant
        fields = (
            'id',
            'availability',
            'reputation',
            'is_active',
            'technical_support_completed',
            'loans_completed',
            'maintenance_completed',
        )
        read_only_fields = (
            'reputation',
            'technical_support_completed',
            'loans_completed',
            'maintenance_completed',
        )
