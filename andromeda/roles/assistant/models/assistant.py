"""Modelo del auxiliar de sistemas."""

# Django
from django.db import models

# Utilidades
from andromeda.utils.models import AndromedaModel


class Assistant(AndromedaModel):
    """Modelo del auxiliar de sistemas

    Extiende de AndromedaModel y agrega nuevos campos para
    el rol de auxiliar de sistemas, que se encargara de todos
    los servicios habilitados por el sistema, solo puede completar un servicio
    a la vez para evitar el exceso de trabajo y saturación de solicitudes para
    el auxiliar de sistemas.
    """

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)

    availability = models.BooleanField(
        default=True,
        help_text='Disponibilidad del auxiliar de sistemas'
    )

    # Estadisticas
    reputation = models.FloatField(
        default=5.0,
        help_text='Reputación del auxiliar basada en la calificación de los servicios completados'
    )

    # Estado
    is_active = models.BooleanField(
        'estado de rol activo',
        default=True,
        help_text='Solo un usuario activo puede interactuar con el sistema'
    )

    # Estadisticas
    technical_support_completed = models.PositiveIntegerField(default=0)
    loans_completed = models.PositiveIntegerField(default=0)
    maintenance_completed = models.PositiveIntegerField(default=0)

    def __str__(self):
        """Regresa un resumen del auxiliar."""
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        """Clase meta."""
        db_table = 'tbl_auxiliar_sistemas'
