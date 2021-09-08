"""Serializer de empleado"""

# Django REST Framework
from rest_framework import serializers

# Modelos
from andromeda.roles.employee.models import Employee


class EmployeeModelSerializer(serializers.ModelSerializer):
    """Serializer del rol de empleado"""

    class Meta:
        """Clase Meta"""
        model = Employee
        fields = (
            'id',
            'work_area',
            'position',
            'technical_support_request',
            'loans_request',
            'is_active',
        )
        read_only_fields = (
            'technical_support_request',
            'loans_request'
        )
