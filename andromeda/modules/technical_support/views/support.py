"""Vista del modulo de soporte tecnico."""

# Utilidades
import environ
# Django REST Framework
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
# Filtros
from rest_framework.filters import SearchFilter, OrderingFilter
# Permisos
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from andromeda.modules.technical_support.permissions import IsServiceOwner, IsPersonalAuthorized

# Modelos
from andromeda.modules.technical_support.models import Support, RatingSupport

# Serializers
from andromeda.modules.technical_support.serializers import (
    SupportModelSerializer,
    CreateSupportSerializer,
    CreateSupportRatingSerializer,
    RatingSupportModelSerializer,
)
# Google Calendar
from andromeda.tasks.google_calendar import google_calendar_service


env = environ.Env()


class SupportViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """View set del modulo de soporte tecnico."""

    # Filtros de busqueda
    filter_backends = (SearchFilter, OrderingFilter)
    ordering = ('support_date', 'complete_support_date', 'assigned_auxiliary', 'support_location')
    ordering_fields = ('support_date', 'complete_support_date', 'assigned_auxiliary', 'support_location')
    search_fields = 'support_location'

    queryset = Support.objects.all()

    def perform_destroy(self, instance):
        """Inactiva el soporte tecnico y elimina
        el evento del calendario de Google Calendar."""

        instance.is_active = False
        instance.status_support = 'Cancelado'
        # Elimina el evento
        google_calendar_service(
            calendar=env('CALENDAR_SUPPORTS'),
            eventId=instance.event_google_id,
            calendarDelete=True
        )
        instance.save()

    def get_serializer_context(self):
        """Contexto"""
        context = super(SupportViewSet, self).get_serializer_context()
        return context

    def get_permissions(self):
        """Asigna los permisos basados en la acción."""
        permissions = [IsAuthenticated]
        if self.action in ['destroy']:
            permissions.append(IsServiceOwner)
        else:
            permissions.append(IsPersonalAuthorized)
        return [p() for p in permissions]

    def get_serializer_class(self):
        """Regresa el serializer basado en la acción."""
        if self.action == 'create':
            return CreateSupportSerializer
        if self.action == 'rate':
            return CreateSupportRatingSerializer
        return SupportModelSerializer

    @action(detail=True, methods=['post'])
    def rate(self, request, *args, **kwargs):
        """Calificación el soporte solicitado."""
        support = self.get_object()
        serializer_class = self.get_serializer_class()
        context = self.get_serializer_context()
        context['support'] = support
        serializer = serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        support = serializer.save()
        data = SupportModelSerializer(support).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def rating(self, request, *args, **kwargs):
        """Soporte calificado"""
        support = self.get_object()
        support_rated = RatingSupport.objects.get(support=support)
        data = RatingSupportModelSerializer(support_rated).data
        return Response(data)
