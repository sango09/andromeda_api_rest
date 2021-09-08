"""Modelo de perfil."""

# Django
from django.db import models

# Utilidades
from andromeda.utils.models import AndromedaModel


class Profile(AndromedaModel):
    """Modelo del perfil de usuario

    Un perfil de usuario tiene datos publicos como la foto, el cargo, el area de trabajo
    y si su rol es auxiliar la calificación de sus servicios.
    """
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    picture = models.ImageField(
        'imagen de perfil',
        default='users/pictures/default-profile.png',
        upload_to='users/pictures/',
        blank=True,
        null=False
    )

    def __str__(self):
        """Regresa la representacion en string del usuario."""
        return str(self.user)

    class Meta:
        """Clase meta."""
        db_table = 'tbl_perfiles'
