"""Modelo de soporte tecnico."""

# Django
from django.db import models

# Utilidades
from andromeda.utils.models import AndromedaModel


class Support(AndromedaModel):
    """Modelo del modulo de soport tecnico

    Extiende de AndromedaModel y agrega nuevos campos para
    solicitar el servicio de soporte tecnico, los principales
    usuarios en solicitarlo, seran los empleados quienes tambien
    podran calificar el servicio al finalizar.
    """

    request_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    assigned_auxiliary = models.ForeignKey('assistant.Assistant', on_delete=models.SET_NULL, null=True)
    auxiliary_id = models.IntegerField(null=True)

    support_location = models.CharField(max_length=50)
    event_google_id = models.CharField(max_length=100, null=True)
    support_date = models.DateTimeField()
    complete_support_date = models.DateTimeField(blank=True, null=True)
    status_support = models.CharField(max_length=50, blank=True, null=True)
    rating = models.FloatField(null=True, blank=True)

    is_active = models.BooleanField(
        'estado de activo',
        default=True,
        help_text='Se utiliza para marcar cuando el soporte fue completado o cancelado'
    )

    description_problem = models.TextField()

    def __str__(self):
        """Regresa los detalles del soporte solicitado."""
        return 'Soporte tecnico registrado para el {_from} |Fecha: {day} {i_time} solicitado por {_user}|{_assistant}'.format(
            _from=self.support_location,
            day=self.support_date.strftime('%a %d, %b'),
            i_time=self.support_date.strftime('%I:%M %p'),
            _user=self.request_by,
            _assistant=self.assigned_auxiliary,
        )

    class Meta:
        """Clase meta."""
        db_table = 'tbl_soporte'
