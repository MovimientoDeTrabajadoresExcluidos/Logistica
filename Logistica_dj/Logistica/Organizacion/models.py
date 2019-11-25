from django.db import models
from django.contrib.auth.models import User
from polymorphic.models import PolymorphicModel


class Punto(PolymorphicModel):
    class Meta:
        verbose_name = "Punto"
        verbose_name_plural = "Puntos"


class PuntoDeRecepcion(Punto):

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

    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=80)
    localidad = models.CharField(max_length=40)
    provincia = models.CharField(max_length=40)
    tipo_de_establecimiento = models.CharField(max_length=20, default='', choices=TIPO_DE_ESTABLECIMIENTO)
    responsable = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    telefono = models.CharField(max_length=20, verbose_name='Teléfono', default="")
    email = models.EmailField(default="")
    observacion = models.TextField(blank=True)

    def __str__(self):
        return "{n} - {te}".format(n=self.nombre, te=self.tipo_de_establecimiento)


class PuntoDeConsumo(Punto):

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
    responsable = models.CharField(max_length=50, default="")
    telefono = models.CharField(max_length=20, verbose_name='Teléfono', default="")
    observacion = models.TextField(blank=True)

    def __str__(self):
        return "{n} - {te}".format(n=self.nombre, te=self.tipo_de_establecimiento)

    def __unicode__(self):
        return self.nombre