# Generated by Django 5.0.6 on 2024-10-05 16:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("facturacion", "0001_initial"),
        ("inventario", "0002_categoria_producto_categoria"),
    ]

    operations = [
        migrations.AlterField(
            model_name="detsale",
            name="producto",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="inventario.producto",
            ),
        ),
    ]
