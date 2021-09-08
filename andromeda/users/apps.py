"""App de usuario."""

# Django
from django.apps import AppConfig


class UserAppConfig(AppConfig):
    """Config del app de usuario."""
    name = 'andromeda.users'
    verbose_name = 'Users'
