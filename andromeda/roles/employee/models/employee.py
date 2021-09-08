"""Modelo de empleado"""

# Django
from django.db import models

# Utilidades
from andromeda.utils.models import AndromedaModel


class Employee(AndromedaModel):
    """Modelo de empleado

    Extiende de AndromedaModel y agrega nuevos campos para
    el rol de empleado, que agrupa los cargos del personal
    administrativo y profesores, quienes seran los principales
    usuarios en solicitar los servicios habilitados por el
    sistema y tendran la opción de calificar el servicio prestamos por
    el auxiliar de sistemas asignado.
    """

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    work_area = models.CharField(
        'area laboral',
        max_length=25
    )

    position = models.CharField(
        'cargo que desempeñan',
        max_length=25
    )

    # Estadisticas
    technical_support_request = models.PositiveIntegerField(default=0)
    loans_request = models.PositiveIntegerField(default=0)

    # Estado
    is_active = models.BooleanField(
        'estado de rol activo',
        default=True,
        help_text='Solo un usuario activo puede interactuar con el sistema'
    )

    def __str__(self):
        """Regresa el area laboral y el cargo que desempeña"""
        return '{} {} desempeña el cargo laboral de {} en el {}'.format(
            self.user.first_name,
            self.user.last_name,
            self.position,
            self.work_area
        )

    class Meta:
        """Clase meta"""
        db_table = 'tbl_empleados'
