from django.db import models
from Proveedores.models import *


class ProductoGenerico(models.Model):

    class Meta:
        verbose_name = "Producto Genérico"
        verbose_name_plural = "Productos Genéricos"
    CATEGORIA = (
        ('Alimento Seco', 'Alimento Seco'),
        ('Alimento Fresco', 'Alimento Fresco'),
        ('Textil', 'Textil'),
        ('Obras', 'Obras'),
        ('Otros', 'Otros'),
    )
    categoria = models.CharField(max_length=15, default='', choices=CATEGORIA)
    tipo = models.CharField(max_length=25, default='')
    UNIDAD_DE_MEDIDA = (
       ('Kilo', 'Kilogramos'),
       ('Litro', 'Litros'),
       ('Unidad', 'Unidad'),
    )
    unidad_de_medida = models.CharField(max_length=15, default='', choices=UNIDAD_DE_MEDIDA)

    def __str__(self):
        return "%s" %(self.tipo)


class VarianteProducto(models.Model):

    class Meta:
        verbose_name = "Variante de Producto"
        verbose_name_plural = "Variantes de Productos"
    tipo = models.ForeignKey(ProductoGenerico, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, default = None)
    denominacion = models.CharField(max_length=40, default='', verbose_name="Denominación del producto por parte del Proveedor")
    cantidad = models.PositiveIntegerField(default=0, verbose_name="Cantidad por unidad")
    pack = models.PositiveIntegerField(default=0, verbose_name="Unidades de empaque")

    def __str__(self):
        return self.denominacion

