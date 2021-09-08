"""Django models utilities."""

# Django
from django.db import models


class AndromedaModel(models.Model):
    """Andromeda base model

    AndromedaModel es una clase abstracta donde otros modelos de
    andromeda pueden heredar. Esta clase proporciona a las tablas
    las siguientes columnas:
        + created (Datetime): Almacena cuando fue creado el registro en la base de datos
        + modified (Datetime): Almacena cuando fue la ultima modificación del registro
            en la base de datos.
    """

    created = models.DateTimeField(
        'creado el',
        auto_now_add=True,
        help_text='Fecha y hora del registro'
    )
    modified = models.DateTimeField(
        'modificado el',
        auto_now=True,
        help_text='Fecha y hora de la ultima modificación'
    )

    class Meta:
        """Opcion Meta."""
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-modified']
