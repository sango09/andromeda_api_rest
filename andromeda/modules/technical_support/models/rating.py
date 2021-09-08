"""Modelo de la calificación del soporte tecnico."""

# Django
from django.db import models

# Utilidades
from andromeda.utils.models import AndromedaModel


class RatingSupport(AndromedaModel):
    """Calificación de servicios

    Almacenera datos cuando el usuario califique de 1 a 5
    la calidad del servicio solicitado y este tendra efecto
    en la reputación del auxiliar asignado para completar el
    servicio solicitado y podra ser analizado por el coordinador
    para la toma de decisiones sobre la calidad de los servicios.
    """

    support = models.ForeignKey(
        'technical_support.Support',
        on_delete=models.CASCADE,
        related_name='rated_support'
    )

    rating_user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True,
        help_text='Usuario que califica el soporte tecnico',
        related_name='rating_user',
    )

    rated_assistant = models.ForeignKey(
        'assistant.Assistant',
        on_delete=models.CASCADE,
        null=True,
        help_text='Auxiliar que recibe la calificación',
        related_name='rated_assistant'
    )

    comments = models.TextField(blank=True)

    rating = models.IntegerField(default=1)

    def __str__(self):
        """Regresa los detalles de la califación."""
        return 'El usuario {} {} califico al {} con {}'.format(
            self.rating_user.first_name,
            self.rating_user.last_name,
            self.rated_assistant,
            self.rating,
        )

    class Meta:
        """Clase meta."""
        db_table = 'tbl_calificacion_soporte'
