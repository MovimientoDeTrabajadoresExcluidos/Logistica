from django.db import models
from django.contrib.auth.models import User


class PuntoDeRecepcion(models.Model):

    class Meta:
        verbose_name = "Punto de Recepción"
        verbose_name_plural = "Punto de Recepción"

    TIPO_DE_ESTABLECIMIENTO = (
        ('Casa Compañero', 'Casa Compañero'),
        ('Centro Barrial', 'Centro Barrial'),
        ('Comendor', 'Comedor'),
        ('Cooperativa', 'Cooperativa'),
        ('Merendero-Comedor', 'Merendero-Comedor'),
    )

    tipo_de_establecimiento = models.CharField(max_length=20, default='', choices=TIPO_DE_ESTABLECIMIENTO)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=80)
    localidad = models.CharField(max_length=40)
    provincia = models.CharField(max_length=40)
    responsable = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    observacion = models.TextField(blank=True)

    def __str__(self):
        return "{n} - {te}".format(n=self.nombre, te=self.tipo_de_establecimiento)


class PuntoDeConsumo(models.Model):

    class Meta:
        verbose_name = "Punto de Consumo"
        verbose_name_plural = "Punto de Consumo"

    TIPO_DE_ESTABLECIMIENTO = (
        ('Casa Comunitaria', 'Casa Comunitaria'),
        ('Centro Barrial', 'Centro Barrial'),
        ('Comendor', 'Comedor'),
        ('Cooperativa', 'Cooperativa'),
        ('Merendero', 'Merendero'),
        ('Merendero-Comedor', 'Merendero-Comedor'),
    )

    nombre =  models.CharField(max_length=50)
    direccion = models.CharField(max_length=80)
    localidad = models.CharField(max_length=40)
    provincia = models.CharField(max_length=40)
    punto_de_recepcion = models.ForeignKey(
        PuntoDeRecepcion,
        on_delete=models.CASCADE,
        default=''
    )
    tipo_de_establecimiento = models.CharField(max_length=20, default='', choices=TIPO_DE_ESTABLECIMIENTO)
    observacion = models.TextField(blank=True)

    def __str__(self):
        return "{n} - {te}".format(n=self.nombre, te=self.tipo_de_establecimiento)
