# Generated by Django 2.2.6 on 2019-10-14 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Movimientos', '0006_auto_20191014_1620'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lineadepedido',
            old_name='scantidad',
            new_name='cantidad',
        ),
    ]
