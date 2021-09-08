"""Modelo de inventario de prestamos tecnologicos."""

# Django
from django.db import models

# Utilidades
from andromeda.utils.models import AndromedaModel


class InventoryLoans(AndromedaModel):
    """Modelo del inventario de prestamos tecnologicos

    Almacenera todos los implementos disponibles para el
    servicio de prestamos tecnologicos, de los cuales tendran
    una cantidad limita y implementos asignados para este
    tipo de servicio.
    """

    implement = models.ForeignKey('inventory.Inventory', on_delete=models.CASCADE)

    implements_available = models.PositiveIntegerField(default=0)
    implements_used = models.PositiveIntegerField(default=0)
    total_implements = models.PositiveIntegerField(default=0)

    last_admission = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Regresa el implemento con su cantidad disponible y en uso."""
        return str(self.implement.name)

    class Meta:
        """Clase meta."""
        db_table = 'tbl_inventario_prestamos'
