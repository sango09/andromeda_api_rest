"""Permisos del modulo de soporte tecnico."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsServiceOwner(BasePermission):
    """Verifica que el usuario es quien solicito el servicio
    o tiene el rol de coordinador."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.request_by or bool(request.user.is_admin)


class IsPersonalAuthorized(BasePermission):
    """Verifica que el usuario es quien solicito
    el servicio o hace parte del personal autorizado"""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.request_by or bool(
            request.user.is_admin or request.user.is_assistant
        )
