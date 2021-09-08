"""Permisos de usuarios."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    """Permite el acceso solo a los propietarios
    de las cuentas que hace la solicitud."""

    def has_object_permission(self, request, view, obj):
        """Verifica el obj y usuario sean los mismos"""
        return request.user == obj or bool(request.user.is_admin)


class IsAdmin(BasePermission):
    """Permite el acceso solo a los usuarios con el rol de
    coordinador."""

    def has_permission(self, request, view):
        """Verifica que el usuario sea coordinador."""
        return bool(request.user.is_admin)
