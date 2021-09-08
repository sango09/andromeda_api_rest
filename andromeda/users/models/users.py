"""Modelo de usuarios."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Utilidades
from andromeda.utils.models import AndromedaModel


class User(AndromedaModel, AbstractUser):
    """Modelo de usuarios

    Extiende de Django's Abstract User, cambiando el campo de username
    por email como metodo de acceso y agregando algunas campos extras
    para el registro de usuarios.
    """
    email = models.EmailField(
        'correo electronico',
        unique=True,
        error_messages={
            'unique': 'Este usuario ya fue registrado'
        }
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    is_client = models.BooleanField(
        'cliente',
        default=True,
        help_text=(
            'Ayuda a distinguir facilmente a los usuarios registrados y sus roles '
        )
    )

    # Roles
    is_admin = models.BooleanField(
        'coordinador',
        default=False,
        help_text=(
            'Rol de coordinador, tiene los permisos generales del sistema'
        )
    )
    is_employee = models.BooleanField(
        'empleados',
        default=False,
        help_text=(
            'Rol de empleado, agrupando administrativos y profesores en un solo rol'
        )
    )
    is_assistant = models.BooleanField(
        'auxiliar de sistemas',
        default=False,
        help_text=(
            'Rol de auxiliar de sistemas, tiene los permisos basicos para utilizar el sistema'
        )
    )

    # Estado de verificación
    is_verified = models.BooleanField(
        'verificado',
        default=True,
        help_text='Se establece como verdadero cuando el usuario confirma su correo electronico'
    )

    def __str__(self):
        """Regresa el username."""
        return self.username

    def get_short_name(self):
        """Regresa el username."""
        return self.username

    class Meta:
        """Clase meta."""
        db_table = 'tbl_usuarios'
