from django.db import models


class Producto(models.Model):

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Producto"

    TIPO = (
        ('Alimento Seco', 'Alimento Seco'),
        ('Alimento Fresco', 'Alimento Fresco'),
        ('Textil', 'Textil'),
        ('Obras', 'Obras'),
        ('Otros', 'Otros'),
    )
    tipo = models.CharField(max_length=15, default='', choices=TIPO)
    denominacion = models.CharField(default='', max_length=50)
    UNIDAD_DE_MEDIDA = (
       ('Kilo', 'Kilogramos'),
       ('Litro', 'Litros'),
       ('Unidad','Unidad')
    )
    unidad_de_medida = models.CharField(max_length=15, default='', choices=UNIDAD_DE_MEDIDA)
    cantidad = models.FloatField(default=0 , verbose_name='Cantidad')

    def __str__(self):
        return "{} - {} {}".format(self.denominacion, self.cantidad, self.unidad_de_medida)

