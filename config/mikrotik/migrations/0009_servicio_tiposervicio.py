# Generated by Django 4.2.5 on 2024-07-08 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mikrotik", "0008_servicio_zona"),
    ]

    operations = [
        migrations.AddField(
            model_name="servicio",
            name="tiposervicio",
            field=models.CharField(
                choices=[("Activo", "Activo"), ("Inactivo", "Inactivo")],
                default="IP estatica",
                max_length=12,
            ),
        ),
    ]