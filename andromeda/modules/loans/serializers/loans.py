"""Serializer para los prestamos tecnologicos."""

from datetime import timedelta

# Utilidades
import environ
# Django
from django.utils import timezone
# Django REST Framework
from rest_framework import serializers

from andromeda.modules.loans.models import Loans, InventoryLoans
# Serializers
from andromeda.modules.loans.serializers.inventory_loans import InventoryLoansSerializer
from andromeda.roles.assistant.models import Assistant
# Modelos
from andromeda.roles.employee.models import Employee
# Tareas
from andromeda.tasks.google_calendar import schedule_service
from andromeda.users.serializers import UserModelSerializer
from andromeda.utils.utils import get_assistant_asigned

env = environ.Env()
GOOGLE_CALENDAR_ID_LOANS = env('CALENDAR_LOANS')


class LoansModelSerializer(serializers.ModelSerializer):
    """Serializer base para el modulo de prestamos tecnologicos."""

    request_by = UserModelSerializer(read_only=True)
    assigned_auxiliary = serializers.StringRelatedField()
    implement = InventoryLoansSerializer(read_only=True)

    class Meta:
        """Clase meta"""
        model = Loans
        fields = '__all__'
        read_only_fields = (
            'request_by',
            'assigned_auxiliary',
            'implement'
        )

    def update(self, instance, data):
        """Permite actualizar el prestamos antes de la fecha del servicio."""
        complete_loans_date = data.get('complete_loans_date', None)
        loans_location = data.get('loans_location', instance.loans_location)
        loans_date = data.get('loans_date', instance.loans_date)
        ammount_implements = data.get('ammount_implements', instance.ammount_implements)
        implement = data.get('implement', instance.implement)
        comments = data.get('comments', instance.comments)

        if instance.complete_loans_date and instance.is_active is False:
            raise serializers.ValidationError('El prestamo tecnologico ya fue completado y no puede ser modificado')

        if instance.is_active is False:
            raise serializers.ValidationError('El prestamo tecnologico fue cancelado y no puede ser modificado')

        if complete_loans_date:
            min_date = instance.loans_date + timedelta(minutes=60)
            if complete_loans_date < min_date and self.context['request'].user.is_assistant:
                raise serializers.ValidationError(
                    'El prestamo tecnologico no puede ser completado por un auxiliar antes de la hora solicitada'
                )
            if instance.request_by.is_employee:
                # Estadisticas de empleado
                employee = Employee.objects.get(user_id=instance.request_by.id)
                employee.loans_request += 1
                employee.save()

            # Actualización de estadisticas del auxiliar
            assistant = Assistant.objects.get(pk=instance.auxiliary_id)
            assistant.loans_completed += 1
            assistant.save()

            # Actualización del inventario
            implement = InventoryLoans.objects.get(id=instance.implement.id)
            implement.implements_available += instance.ammount_implements
            implement.implements_used -= instance.ammount_implements
            implement.save()

            # Estado del prestamos
            instance.status_loans = 'Completado'
            instance.save()

        else:
            # Actualización del evento en el calendario de Google Calendar
            schedule_service(
                summary=f'{ammount_implements}X {implement}',
                location=loans_location,
                comments=comments,
                event_date=loans_date,
                calendar_id=GOOGLE_CALENDAR_ID_LOANS,
                update_event=True,
                event_id=instance.event_google_id
            )
        return super(LoansModelSerializer, self).update(instance, data)


class CreateLoansSerializer(serializers.ModelSerializer):
    """Serializer para agendar un prestamo."""

    request_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    assigned_auxiliary = serializers.StringRelatedField()

    class Meta:
        """Clase Meta"""
        model = Loans
        exclude = ('complete_loans_date', 'is_active')

    def validate_loans_date(self, data):
        """Verifica que el servicio sea solicitado en un tiempo valido."""
        min_date = timezone.now() + timedelta(minutes=120)
        if data < min_date:
            raise serializers.ValidationError(
                'El prestamo tecnologico debe ser solicitado minimo con 2 horas de anticipación'
            )
        return data

    def validate(self, data):
        """Validación

        Verifica que sea el mismo usuario validado quien solicita el servicio.
        """
        implements_available = data['implement'].implements_available
        if implements_available <= 0:
            raise serializers.ValidationError('No hay implementos disponibles :(')

        if data['ammount_implements'] > implements_available:
            raise serializers.ValidationError(
                f'No se pueden solicitar mas equipos de los disponibles: {implements_available}'
            )

        if self.context['request'].user != data['request_by']:
            raise serializers.ValidationError(
                'El prestamo tecnologico solo puede ser solicitado por el usuario autenticado'
            )
        return data

    def create(self, data):
        """Crea el servicio de prestamos tecnologicos, actualiza el inventario de prestamos
        y agenda el evento en el calendario de prestamos tecnologicos de google."""
        ammount_implements = data.get('ammount_implements')
        implement = data.get('implement')
        comments = data.get('comments', '')

        service_event = schedule_service(
            summary=f'{ammount_implements}X {implement}',
            location=data['loans_location'],
            comments=comments,
            event_date=data['loans_date'],
            calendar_id=GOOGLE_CALENDAR_ID_LOANS
        )

        # Inventario de prestamos
        implement.implements_available -= ammount_implements
        implement.implements_used += ammount_implements
        implement.save()

        loans = Loans.objects.create(
            **data,
            assigned_auxiliary=get_assistant_asigned(),
            event_google_id=service_event,
            status_loans='En proceso'
        )
        loans.auxiliary_id = loans.assigned_auxiliary.pk
        loans.save()

        return loans
