# Generated by Django 2.2.6 on 2019-10-21 22:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Movimientos', '0017_auto_20191021_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='egresospuntoderecepcion',
            name='destino',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Organizacion.PuntoDeConsumo'),
        ),
        migrations.AlterField(
            model_name='egresospuntoderecepcion',
            name='origen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Organizacion.PuntoDeRecepcion'),
        ),
    ]
