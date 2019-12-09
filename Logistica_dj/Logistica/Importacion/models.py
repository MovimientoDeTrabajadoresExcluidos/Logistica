from django.db import models
from Movimientos.models import IngresosAPuntosDeRecepcion, EgresosPuntoDeRecepcion, Distribucion


# Create your models here.
class ImportacionLineaIngreso(models.Model):
    class Meta:
        verbose_name = 'Importacion Linea de Ingreso'
        verbose_name_plural = 'Importacion Lineas de Ingreso'

    ingreso = models.ForeignKey(IngresosAPuntosDeRecepcion, on_delete=models.CASCADE)
    documento = models.FileField()

    def __str__(self):
        return str(self.ingreso)

    def delete(self, using=None, keep_parents=False):
        self.documento.delete()  # esto es para borrar el archivo que por alguna razon no lo hace
        return super(ImportacionLineaIngreso, self).delete()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            if self.pk: # si existe elimino el documento anterior (si es el mismo no se borra)
                old_file = ImportacionLineaIngreso.objects.get(pk=self.pk)
                if not old_file.documento == self.documento:
                    old_file.documento.delete()
        except:
            pass # todo ver que se haria si no existe en la bd. creo que no se haria nada
        super(ImportacionLineaIngreso, self).save()


class ImportacionDistribucion(models.Model):
    class Meta:
        verbose_name = 'Importacion de Distribucion'
        verbose_name_plural = 'Importacion de Distribuciones'

    distribucion = models.ForeignKey(Distribucion, on_delete=models.CASCADE)
    documento = models.FileField()

    def __str__(self):
        return str(self.distribucion)

    def delete(self, using=None, keep_parents=False):
        if self.documento:
            self.documento.delete()  # esto es para borrar el archivo que por alguna razon no lo hace
        return super(ImportacionDistribucion, self).delete()
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            if self.pk: # si existe elimino el documento anterior (si es el mismo no se borra)
                old_file = ImportacionDistribucion.objects.get(pk=self.pk)
                if old_file.documento and not old_file.documento == self.documento:
                    old_file.documento.delete()
        except:
            pass # todo ver que se haria si no existe en la bd. creo que no se haria nada
        super(ImportacionDistribucion, self).save()