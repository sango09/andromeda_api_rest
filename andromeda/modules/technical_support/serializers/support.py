"""Serializer del modulo soporte tecnico."""

# Utilidades
import environ
# Django REST Framework
from rest_framework import serializers

# Modelos
from andromeda.modules.technical_support.models import Support
from andromeda.roles.assistant.models import Assistant
from andromeda.roles.employee.models import Employee
# Tareas
from andromeda.tasks.google_calendar import schedule_service
# Serializers
from andromeda.users.serializers import UserModelSerializer
from andromeda.utils import get_assistant_asigned

env = environ.Env()

# Google Calendar ID
GOOGLE_CALENDAR_ID_SUPPORT = env('CALENDAR_SUPPORTS')


class SupportModelSerializer(serializers.ModelSerializer):
    """Serializer para el modulo de soporte tecnico."""
    request_by = UserModelSerializer(read_only=True)
    assigned_auxiliary = serializers.StringRelatedField()

    class Meta:
        """Clase Meta"""
        model = Support
        fields = '__all__'
        read_only_fields = (
            'request_by',
            'assigned_auxiliary',
            'rating'
        )

    def update(self, instance, data):
        """Permite actualizar los datos solo despues de la fecha de solicitud."""
        complete_support_date = data.get('complete_support_date', None)
        support_location = data.get('support_location', instance.support_location)
        description_problem = data.get('description_problem', instance.description_problem)
        support_date = data.get('support_date', instance.support_date)

        if instance.status_support == 'Completado':
            raise serializers.ValidationError('El soporte tecnico ya fue completado y no puede ser modificado')

        if instance.status_support == 'Cancelado':
            raise serializers.ValidationError('El  soporte tecnico fue cancelado y no puede ser modificado')

        if complete_support_date:
            if instance.request_by.is_employee:
                # Estadisticas de empleado
                employee = Employee.objects.get(user_id=instance.request_by.id)
                employee.technical_support_request += 1
                employee.save()

            # Estadisticas de auxiliar asignado
            assistant = Assistant.objects.get(pk=instance.assigned_auxiliary.id)
            assistant.technical_support_completed += 1
            assistant.save()

            # Estado de soporte
            instance.status_support = 'Completado'
            instance.save()

        else:
            # Actualización del event en Google Calendar.
            schedule_service(
                summary=f'Soporte tecnico para {instance.request_by.get_full_name()} en {support_location}',
                location=support_location,
                comments=description_problem,
                event_date=support_date,
                calendar_id=GOOGLE_CALENDAR_ID_SUPPORT,
                update_event=True,
                event_id=instance.event_google_id
            )

        return super(SupportModelSerializer, self).update(instance, data)


class CreateSupportSerializer(serializers.ModelSerializer):
    """Serializer para agendar el soporte tecnico."""

    request_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    assigned_auxiliary = serializers.StringRelatedField()
    support_date = serializers.DateTimeField(format='iso-8601')

    class Meta:
        """Clase meta."""
        model = Support
        exclude = (
            'complete_support_date',
            'is_active',
            'rating'
        )

    def validate(self, data):
        """Valida que el usuario usuario que solicita el servicio sea el mismo que esta logueado."""
        if self.context['request'].user != data['request_by']:
            raise serializers.ValidationError('El soporte tecnico solo puede ser solicitado por el usuario autenticado')
        return data

    def create(self, data):
        """Crea el soporte tecnico y agenda el evento en el calendario de soporte tecnico."""
        support = Support.objects.create(
            **data,
            assigned_auxiliary=get_assistant_asigned(),
            status_support='En proceso'
        )

        # Agenda el Soporte Tecnico en el calendario.
        service_event = schedule_service(
            summary=f'Soporte tecnico para {support.request_by.get_full_name()} en {support.support_location}',
            location=support.support_location,
            comments=support.description_problem,
            event_date=support.support_date,
            calendar_id=GOOGLE_CALENDAR_ID_SUPPORT
        )

        support.auxiliary_id = support.assigned_auxiliary.pk
        support.event_google_id = service_event
        support.save()

        return support
