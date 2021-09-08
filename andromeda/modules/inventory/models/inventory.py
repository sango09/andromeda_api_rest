"""Modelo del inventario."""

# Django
from django.db import models

# Utilidades
from andromeda.utils.models import AndromedaModel


class TechnicalDataSheet(AndromedaModel):
    """Modelo de la ficha tecnica de un implemento tecnologico

    Esta ficha tecnica agregara los campos requeridos para que el
    usuario sepa las especificacion tecnicas del equipo a solicitar.
    """
    picture = models.ImageField(
        default='inventory/pictures/default-image.png',
        upload_to='inventory/pictures',
        blank=True,
        null=True,
    )

    brand_implement = models.CharField(max_length=50, null=False)
    model_implement = models.CharField(max_length=50, null=False)
    operating_system = models.CharField(max_length=50, null=True, blank=True)
    specifications = models.TextField(
        null=False,
        help_text='Especificaciones tecnicas del implemento'
    )

    def __str__(self):
        """Regresa el modelo."""
        return self.model_implement

    class Meta:
        """Clase meta."""
        db_table = 'tbl_ficha_tecnica'


class Inventory(AndromedaModel):
    """Modelo del inventario

    Almacenara a todos los implementos registrados previamente y de los cuales
    tienen un ficha tecnica que tiene todas las especificaciones tecnicas del
    implemento, los campos economicos y las cantidades seran almacenadas por este
    modelo.
    """
    name = models.CharField(max_length=70, help_text='Nombre del implemento')
    category = models.CharField(max_length=50, help_text='Categoria a la pertenece el implemento')
    technical_data_sheet = models.ForeignKey('inventory.TechnicalDataSheet', on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=50, unique=True, null=False)
    purchase_date = models.DateField()
    price = models.CharField(max_length=50)
    assigned_user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    status_implement = models.CharField(max_length=40, null=False)

    def __str__(self):
        return f'Implemento {self.name} con numero de serie {self.serial_number}'

    class Meta:
        """Clase meta."""
        db_table = 'tbl_inventario'
