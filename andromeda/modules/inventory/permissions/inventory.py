"""Permisos del modulo de inventario."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):
    """Verifica que el usuario tenga el rol de auxiliar de Sistemas
    o coordinador."""

    def has_permission(self, request, view):
        """Verifica que el usuario sea auxiliar de sistemas o coordinador."""
        return bool(request.user.is_assistant or request.user.is_admin)


class IsAdmin(BasePermission):
    """Permite realizar el CRUD al usuario con el rol de coordinador."""

    def has_permission(self, request, view):
        """Verifica que el usuario sea coordinador."""
        return bool(request.user.is_admin)
