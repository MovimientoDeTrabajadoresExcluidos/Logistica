from django.db import models

# Create your models here.

class Provincia(models.Model):

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincia"
        ordering = ["-nombre"]
    id_prov = models.PositiveIntegerFieldPrimaryKey()

    def __str__(self):
        return


