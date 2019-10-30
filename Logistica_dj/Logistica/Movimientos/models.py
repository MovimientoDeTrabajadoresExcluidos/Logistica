from django.db import models
from django.utils import timezone
from Proveedores.models import Proveedor
from Organizacion.models import *
from Productos.models import Producto

# Create your models here.

class IngresosAPuntosDeRecepcion(models.Model):

    class Meta:
        verbose_name = "Ingresos a Punto de Recepción"
        verbose_name_plural = "Ingresos a Punto de Recepción"
        ordering = ["-fecha_y_hora_de_registro"]

    origen = models.ForeignKey(Proveedor, on_delete=models.CASCADE, )
    destino = models.ForeignKey(PuntoDeRecepcion, on_delete=models.CASCADE, )#default = PR ASOCIADO AL USUARIO HACER !!!)
    ESTADOS = (
        ("Borrador","Borrador"),
        ("Validado","Validado"),
    )
    fecha_y_hora_de_ingreso = models.DateTimeField(
        default=timezone.now,
    )
    estado = models.CharField(max_length= 9, choices=ESTADOS, default= 'Borrador')
    fecha_y_hora_de_registro = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )

    def __str__(self):
        return "IN-PR #{}".format(str(id(self)))


class EgresosPuntoDeRecepcion(models.Model):

    class Meta:
        verbose_name = "Egreso Punto de Recepción"
        verbose_name_plural = "Egreso Punto de Recepción"
        ordering = ["-fecha_y_hora_de_registro"]

    origen = models.ForeignKey(PuntoDeRecepcion, on_delete=models.CASCADE, )#default = PR ASOCIADO AL USUARIO HACER !!!)
    destino = models.ForeignKey(PuntoDeConsumo, on_delete=models.CASCADE, )
    ESTADOS = (
        ("Borrador","Borrador"),
        ("Validado","Validado"),
    )

    estado = models.CharField(max_length= 9, choices=ESTADOS, default= 'Borrador')
    fecha_y_hora_de_egreso = models.DateTimeField(
        default=timezone.now,
    )
    fecha_y_hora_de_registro = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )

    def __str__(self):
        return "EG-PR #{}".format(str(id(self)))



class LineaDeIng(models.Model):
    class Meta:
        verbose_name = "Línea de Ingreso a PR"
        verbose_name_plural = "Líneas de Ingreso a PR"
    movimiento = models.ForeignKey(IngresosAPuntosDeRecepcion, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    cantidad = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return "ING-PR #{}".format(str(id(self)))

class LineaDeEgr(models.Model):
    class Meta:
        verbose_name = "Línea de Egreso de PR"
        verbose_name_plural = "Líneas de Egreso de PR"
    movimiento = models.ForeignKey(EgresosPuntoDeRecepcion, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    cantidad = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return "EG-PR #{}".format(str(id(self)))