# Generated by Django 2.2.6 on 2019-10-15 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Movimientos', '0013_auto_20191015_1113'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lineadeegr',
            options={'verbose_name': 'Línea de Egreso de PR', 'verbose_name_plural': 'Líneas de Egreso de PR'},
        ),
        migrations.AlterModelOptions(
            name='lineadeing',
            options={'verbose_name': 'Línea de Ingreso a PR', 'verbose_name_plural': 'Líneas de Ingreso a PR'},
        ),
    ]
