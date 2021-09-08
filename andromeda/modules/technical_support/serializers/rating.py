"""Serializer de la calificacion del soporte tecnico."""

# Django
from django.db.models import Avg
# Django REST Framework
from rest_framework import serializers

# Modelos
from andromeda.modules.technical_support.models import RatingSupport
from andromeda.users.serializers import (
    UserModelSerializer,
    AssistantModelSerializer
)


class RatingSupportModelSerializer(serializers.ModelSerializer):
    """Serializer modelo de calificación de soporte"""

    support = serializers.StringRelatedField()
    rating_user = UserModelSerializer(read_only=True)
    rated_assistant = AssistantModelSerializer(read_only=True)

    class Meta:
        """Clase Meta."""
        model = RatingSupport
        fields = '__all__'
        read_only_fields = (
            'support',
            'rating_user',
            'rated_assistant',
            'rating',
            'comments'
        )


class CreateSupportRatingSerializer(serializers.ModelSerializer):
    """Serializer para crear la calificacion del soporte tecnico agendando."""

    rating = serializers.IntegerField(min_value=1, max_value=5)
    comments = serializers.CharField(required=False)

    class Meta:
        """Clase meta"""
        model = RatingSupport
        fields = ('rating', 'comments')

    def validate(self, data):
        """Valida que el soporte no tenga una calificación almacenada."""
        user = self.context['request'].user
        support = self.context['support']

        q = RatingSupport.objects.filter(
            support=support,
            rating_user=user,
        )

        if q.exists():
            raise serializers.ValidationError('El servicio ya fue calificado')
        return data

    def create(self, data):
        """Calcula la calificación del servicio y la calificación base del auxiliar asignado."""
        assigned_auxiliary = self.context['support'].assigned_auxiliary

        RatingSupport.objects.create(
            support=self.context['support'],
            rating_user=self.context['request'].user,
            rated_assistant=assigned_auxiliary,
            **data
        )

        ride_avg = round(
            RatingSupport.objects.filter(
                support=self.context['support']
            ).aggregate(Avg('rating'))['rating__avg'],
            1
        )
        self.context['support'].rating = ride_avg
        self.context['support'].save()

        auxiliary_avg = round(
            RatingSupport.objects.filter(
                rated_assistant=assigned_auxiliary,
            ).aggregate(Avg('rating'))['rating__avg'],
            1
        )

        assigned_auxiliary.reputation = auxiliary_avg
        assigned_auxiliary.save()

        return self.context['support']
