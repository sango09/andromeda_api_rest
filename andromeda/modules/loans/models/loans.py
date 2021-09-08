"""Modelo de prestamos tecnologicos."""

# Django
from django.db import models

# Utitlidades
from andromeda.utils.models import AndromedaModel


class Loans(AndromedaModel):
    """Modelo de modulo de prestamos tecnologicos

    Extiende de AndromedaModel, y agrega nuevos campos
    para solicitar el servicio de prestamos tecnologicos,
    los implementos disponibles hacen parte del inventario
    de prestamos, de los cuales de acuerdo a la solicitud del usuario
    se descontaran y se asignara un auxiliar encargado de
    completar la solicitud del usuario con los implementos
    solicitados.
    """

    request_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    assigned_auxiliary = models.ForeignKey('assistant.Assistant', on_delete=models.SET_NULL, null=True)
    auxiliary_id = models.IntegerField(null=True)

    loans_location = models.CharField(max_length=50)
    event_google_id = models.CharField(max_length=100, null=True)
    loans_date = models.DateTimeField()
    complete_loans_date = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(
        'estado de activo',
        default=True,
        help_text='Se utiliza para marcar cuando el soporte fue completado o cancelado'
    )

    comments = models.TextField(null=True, blank=True)
    status_loans = models.CharField(max_length=50, blank=True, null=True)
    implement = models.ForeignKey('loans.InventoryLoans', on_delete=models.CASCADE)
    ammount_implements = models.PositiveIntegerField(null=False, blank=False)
    ticket = models.FileField(upload_to='tickets/reports/', null=False, blank=True)

    def __str__(self):
        """Regresa los detalles del prestamo tecnologico."""
        return 'Prestamo tecnologico solicitado por {_user} | ' \
               '{ammount} {implement} para el {day} {i_time} | {_assistant}'.format(
                _user=self.request_by,
                ammount=self.ammount_implements,
                implement=self.implement,
                day=self.loans_date.strftime('%a %d, %b'),
                i_time=self.loans_date.strftime('%I:%M %p'),
                _assistant=self.assigned_auxiliary,
                )

    class Meta:
        """Clase meta."""
        db_table = 'tbl_prestamos'
