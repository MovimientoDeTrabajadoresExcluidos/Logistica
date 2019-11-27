from django.db import models
from django.utils import timezone
from Proveedores.models import Proveedor
from Organizacion.models import *
from Productos.models import ProductoGenerico, VarianteProducto


# Create your models here.
class Distribucion(models.Model):
    class Meta:
        verbose_name = "Distribucion"
        verbose_name_plural = "Distribuciones"
    denominacion = models.CharField(max_length=50)
    # TODO eliminar la linea siguiente cuando todo funcione
    # ingreso = models.ForeignKey(IngresosAPuntosDeRecepcion, on_delete=models.CASCADE, verbose_name="Ingreso", default="")
    fecha_de_creacion = models.DateField(default=timezone.now)
    punto_de_recepcion_asociado = models.ForeignKey(PuntoDeRecepcion, on_delete=models.CASCADE)

    def __str__(self):
        return self.denominacion


class DistribucionProducto(models.Model):
    class Meta:
        verbose_name = "Distribucion Producto"
        verbose_name_plural = "Distribuciones Productos"

    producto = models.ForeignKey(VarianteProducto, on_delete=models.CASCADE, verbose_name="Producto", default="",
                                 blank=True)
    distribucion = models.ForeignKey(Distribucion, on_delete=models.CASCADE, verbose_name="Distribucion", default="")
    total_asignado = models.FloatField(default=0, help_text="")

    def __str__(self):
        return "D-Prod #{}".format(str(self.id))


class LineaDistribucionProducto(models.Model):
    class Meta:
        verbose_name = "Linea de Distribucion de Producto"
        verbose_name_plural = "Lineas de Distribucion de Productos"

    distribucion = models.ForeignKey(DistribucionProducto, on_delete=models.CASCADE)
    pc = models.ForeignKey(PuntoDeConsumo, on_delete=models.CASCADE, verbose_name="Punto de Consumo")
    porcentaje = models.FloatField(default=0)  # deberia ser solo positivo

    def __str__(self):
        return "LD-Prod #{}".format(str(self.id))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            estado_anterior = LineaDistribucionProducto.objects.get(id=self.id)
            total_asignado = self.traerTotalAsignado() - estado_anterior.porcentaje + self.porcentaje
            if self.porcentaje < 0 or self.porcentaje > 100 or total_asignado > 100:
                self.porcentaje = estado_anterior.porcentaje
            else:  # si esta en 100% y suma a linea 1 y resta a linea 2 solo se me esta guardando linea 2
                distribucion_producto = DistribucionProducto.objects.get(id=self.distribucion_id)
                distribucion_producto.total_asignado = total_asignado
                distribucion_producto.save()

        except LineaDistribucionProducto.DoesNotExist:
            total_asignado = self.traerTotalAsignado() + self.porcentaje # puede fallar si es mayor a 100
            if self.porcentaje < 0 or self.porcentaje > 100 or total_asignado > 100:
                self.porcentaje = 0
            else:  # si esta en 100% y suma a linea 1 y resta a linea 2 solo se me esta guardando linea 2
                distribucion_producto = DistribucionProducto.objects.get(id=self.distribucion_id)
                distribucion_producto.total_asignado = total_asignado
                distribucion_producto.save()

        finally:
            return super(LineaDistribucionProducto, self).save()

    def traerTotalAsignado(self):
        total = 0
        for pc in LineaDistribucionProducto.objects.filter(distribucion_id=self.distribucion_id):
            total += pc.porcentaje
        return total

# TODO eliminar las listas de destinos
class ListaDestinosEgreso(models.Model):
    class Meta:
        verbose_name = "Lista de Destinos"
        verbose_name_plural = "Listas de Destinos"

    denominacion = models.CharField(max_length=20)
    puntoDeRecepcion = models.ForeignKey(PuntoDeRecepcion, on_delete=models.CASCADE)
    ultima_modificacion = models.DateField(default=timezone.now,)

    def __str__(self):
        return self.denominacion


class LineaListaDestinosEgreso(models.Model):
    class Meta:
        verbose_name = "Linea de Destino"
        verbose_name_plural = "Lineas de Destino"

    listaDeDestinos = models.ForeignKey(ListaDestinosEgreso, on_delete=models.CASCADE)
    puntoDeConsumo = models.ForeignKey(PuntoDeConsumo, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return 'LD - #{}'.format(self.id)


class IngresosAPuntosDeRecepcion(models.Model):
    class Meta:
        verbose_name = "Ingresos a Punto de Recepción"
        verbose_name_plural = "Ingresos a Punto de Recepción"
        ordering = ["-fecha_y_hora_de_registro"]

    origen = models.ForeignKey(Proveedor, on_delete=models.CASCADE, default="")
    destino = models.ForeignKey(PuntoDeRecepcion, on_delete=models.CASCADE,
                                default="")  # default = PR ASOCIADO AL USUARIO HACER !!!)
    ESTADOS = (
        ("Borrador", "Borrador"),
        ("Validado", "Validado"),
    )
    fecha_y_hora_de_ingreso = models.DateTimeField(
        default=timezone.now,
    )
    estado = models.CharField(max_length=9, choices=ESTADOS, default='Borrador')
    fecha_y_hora_de_registro = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )

    # TODO eliminar la linea siguiente cuando todo funcione
    # listaDeDestinos = models.ForeignKey(ListaDestinosEgreso, on_delete=models.CASCADE, default="")
    distribucion = models.ForeignKey(Distribucion, on_delete=models.CASCADE)

    def __str__(self):
        return "IN-PR #{}".format(str(self.id))


class EgresosPuntoDeRecepcion(models.Model):
    class Meta:
        verbose_name = "Egreso Punto de Recepción"
        verbose_name_plural = "Egreso Punto de Recepción"
        ordering = ["-fecha_y_hora_de_registro"]

    origen = models.ForeignKey(PuntoDeRecepcion, on_delete=models.CASCADE,
                               default="")  # default = PR ASOCIADO AL USUARIO HACER !!!)
    destino = models.ForeignKey(PuntoDeConsumo, on_delete=models.CASCADE, default="")
    ESTADOS = (
        ("Borrador", "Borrador"),
        ("Validado", "Validado"),
    )

    estado = models.CharField(max_length=9, choices=ESTADOS, default='Borrador')
    fecha_y_hora_de_egreso = models.DateTimeField(
        default=timezone.now,
    )
    fecha_y_hora_de_registro = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )
    ingreso_asociado = models.ForeignKey(IngresosAPuntosDeRecepcion, on_delete=models.CASCADE)

    def __str__(self):
        return "EG-PR #{}".format(str(self.id))


class LineaDeIng(models.Model):
    class Meta:
        verbose_name = "Línea de Ingreso a PR"
        verbose_name_plural = "Líneas de Ingreso a PR"

    movimiento = models.ForeignKey(IngresosAPuntosDeRecepcion, on_delete=models.CASCADE, default="")
    producto = models.ForeignKey(VarianteProducto, on_delete=models.CASCADE, verbose_name='Producto', default="",
                                 blank=True)
    cantidad = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "ING-PR #{}".format(str(self.id))


class LineaDeEgr(models.Model):
    class Meta:
        verbose_name = "Línea de Egreso de PR"
        verbose_name_plural = "Líneas de Egreso de PR"

    movimiento = models.ForeignKey(EgresosPuntoDeRecepcion, on_delete=models.CASCADE, default="")
    producto = models.ForeignKey(VarianteProducto, on_delete=models.CASCADE, verbose_name='Producto', default="",
                                 blank=True)
    cantidad = models.FloatField(default=0)

    def __str__(self):
        return "EG-PR #{}".format(str(self.id))

