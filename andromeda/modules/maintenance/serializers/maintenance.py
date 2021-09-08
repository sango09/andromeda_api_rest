"""Serializer del modulo de mantenimiento."""

# Utilidades
import environ
# Django REST Framework
from rest_framework import serializers

from andromeda.modules.inventory.models import Inventory
from andromeda.modules.inventory.serializers import InventorySerializer
# Modelos
from andromeda.modules.maintenance.models import Maintenance
from andromeda.roles.assistant.models import Assistant
# Tareas
from andromeda.tasks.google_calendar.google_calendar import schedule_service
# Serializers
from andromeda.users.serializers import UserModelSerializer
from andromeda.utils.utils import get_assistant_asigned

env = environ.Env()

# Google Calendar ID
GOOGLE_CALENDAR_ID_MAINTENANCE = env('CALENDAR_MAINTENANCES')


class MaintenanceModelSerializer(serializers.ModelSerializer):
    """Serializer base para el modulo de mantenimientos preventivos y/o correctivos."""

    request_by = UserModelSerializer(read_only=True)
    assigned_auxiliary = serializers.StringRelatedField()
    implement = InventorySerializer(read_only=True)

    class Meta:
        """Clase meta"""
        model = Maintenance
        fields = '__all__'

        read_only_fields = (
            'request_by',
            'assigned_auxiliary',
        )

    def update(self, instance, data):
        """Actualiza los datos del modulo de inventario y valida las fechas del servicio."""
        complete_maintenance_date = data.get('complete_maintenance_date', None)
        maintenance_type = data.get('maintenance_type', instance.maintenance_type)
        implement = data.get('implement', instance.implement)
        maintenance_location = data.get('maintenance_location', instance.maintenance_location)
        description = data.get('description', instance.description)
        maintenance_date = data.get('maintenance_date', instance.maintenance_date)

        if instance.complete_maintenance_date and instance.is_active is False:
            raise serializers.ValidationError('El mantenimiento ya fue completado y no puede ser modificado')

        if instance.is_active is False:
            raise serializers.ValidationError('El mantenimiento fue cancelado y no puede ser modificado')

        if complete_maintenance_date:
            maintenance_date_format = instance.maintenance_date.strftime('%Y-%m-%d')
            complete_date_format = complete_maintenance_date.strftime('%Y-%m-%d')

            if complete_date_format < maintenance_date_format and self.context['request'].user.is_assistant:
                raise serializers.ValidationError(
                    'El mantenimiento no puede ser completado por un auxiliar antes de la fecha agendada'
                )

            # Estadisticas del auxiliar
            assistant = Assistant.objects.get(pk=instance.auxiliary_id)
            assistant.maintenance_completed += 1
            assistant.save()

            # Estado del implemento
            implement = Inventory.objects.get(pk=instance.implement_id)
            implement.status_implement = 'Disponible'
            implement.save()

            # Estado del mantenimiento
            instance.status_maintenance = 'Completado'
            instance.save()

        else:
            # Actualización del evento en el calendario de Google Calendar
            schedule_service(
                summary=f'Mantenimiento {maintenance_type} al {implement} en {maintenance_location}',
                location=maintenance_location,
                comments=description,
                event_date=maintenance_date,
                calendar_id=GOOGLE_CALENDAR_ID_MAINTENANCE,
                update_event=True,
                event_id=instance.event_google_id
            )

        return super(MaintenanceModelSerializer, self).update(instance, data)


class CreateMaintenanceSerializer(serializers.ModelSerializer):
    """Serialier para agendar un mantenimiento en el sistema."""

    request_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    assigned_auxiliary = serializers.StringRelatedField()

    class Meta:
        """Clase meta"""
        model = Maintenance
        exclude = ('complete_maintenance_date', 'is_active')

    def validate(self, data):
        """Valida que el mantenimiento sea solamente agendado por el usuario logueado."""
        if self.context['request'].user != data['request_by']:
            raise serializers.ValidationError('El mantenimiento solo puede ser solicitado por el usuario autenticado')
        return data

    def create(self, data):
        """Agenda el mantenimiento y actualiza el estado del implemento."""
        implement = data.get('implement')
        maintenance_type = data.get('maintenance_type')
        maintenance_location = data.get('maintenance_location')
        description = data.get('description', '')

        # Agenda el mantenimiento en el calendario de Google Calendar
        service_event = schedule_service(
            summary=f'Mantenimiento {maintenance_type} al {implement} en {maintenance_location}',
            location=maintenance_location,
            comments=description,
            event_date=data['maintenance_date'],
            calendar_id=GOOGLE_CALENDAR_ID_MAINTENANCE
        )

        # Actualizacion del estado en el implemento
        implement.status_implement = 'En mantenimiento'
        implement.save()

        maintenance = Maintenance.objects.create(
            **data,
            assigned_auxiliary=get_assistant_asigned(),
            event_google_id=service_event,
            status_maintenance='En proceso'
        )
        maintenance.auxiliary_id = maintenance.assigned_auxiliary.pk
        maintenance.save()

        return maintenance
