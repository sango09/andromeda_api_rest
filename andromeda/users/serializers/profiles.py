"""Serializer de perfiles."""

# Django REST Framework
from rest_framework import serializers

# Modelos
from andromeda.users.models import Profile


class ProfileModelSerializer(serializers.ModelSerializer):
    """Modelo del serializer para el perfil de usuarios."""

    class Meta:
        """Clase meta."""
        model = Profile
        fields = ('picture',)
