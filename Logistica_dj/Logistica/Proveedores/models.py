from django.db import models
from Organizacion.models import PuntoDeRecepcion

# Create your models here.


class Proveedor(models.Model):

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedor"

    TIPO_DE_PROVEEDOR = (
        ('Boca Nación', 'Boca Nación'),
        ('Convenio Merienda', 'Convenio Merienda'),

    )
    nombre_compania_o_entidad = models.CharField(max_length=50, default='') #verbose = "Nombre de Compañía o Entidad "
    tipo_de_proveedor = models.CharField(max_length=20, default='', choices=TIPO_DE_PROVEEDOR)
    ubicacion = models.CharField(max_length=80, default='')
    localidad = models.CharField(max_length=40, default='')
    provincia = models.CharField(max_length=40, default='')
    #puntos_de_recepcion_asociados = models.ManyToManyField('PuntoDeRecepcion')
    nombre_contacto = models.CharField(max_length=40, default='')
    telefono = models.CharField(max_length=50, verbose_name='Teléfono', default="")
    email = models.EmailField(default="")
    observacion = models.TextField(default= '', blank=True)

    def __str__(self):
        return  "{n} - {tp}" .format(n= self.nombre_compania_o_entidad, tp = self.tipo_de_proveedor)
