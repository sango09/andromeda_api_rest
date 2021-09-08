"""Modelo de mantenimientos."""

# Django
from django.db import models

# Utilidades
from andromeda.utils.models import AndromedaModel


class Maintenance(AndromedaModel):
    """Modelo de mantenimientos

    Solo los usuarios con el rol de auxiliar de sistemas y coordinador
    podran tener acceso al modulo de mantenimientos, podran agendar y cancelar
    los mantenimientos disponibles en el sistema. Cada mantenimiento tiene
    asignado un auxiliar aleatorio.
    """

    request_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    assigned_auxiliary = models.ForeignKey('assistant.Assistant', on_delete=models.SET_NULL, null=True)
    auxiliary_id = models.IntegerField(null=True)

    image_implement = models.ImageField(
        default='inventory/pictures/default-image.png',
        upload_to='maintenance/pictures',
        blank=True,
        null=True
    )

    maintenance_location = models.CharField(max_length=50, help_text='Lugar del mantenimiento')
    event_google_id = models.CharField(max_length=100, null=True)
    maintenance_date = models.DateTimeField()
    maintenance_type = models.CharField(max_length=50)
    implement = models.ForeignKey('inventory.Inventory', on_delete=models.CASCADE)

    status_maintenance = models.CharField(max_length=50, null=True, blank=True)
    complete_maintenance_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=False, null=False)

    is_active = models.BooleanField(
        'estado de activo',
        default=True,
        help_text='Se utiliza para marcar cuando el mantenimiento fue completado o cancelado'
    )

    def __str__(self):
        """Regresa los detalles del mantenimiento."""
        return 'Mantenimiento al {implement} para el {day} {i_time} | {_assistant}'.format(
            implement=self.implement,
            day=self.maintenance_date.strftime('%a %d, %b'),
            i_time=self.maintenance_date.strftime('%I:%M %p'),
            _assistant=self.assigned_auxiliary,
        )

    class Meta:
        """Clase meta."""
        db_table = 'tbl_mantenimientos'
