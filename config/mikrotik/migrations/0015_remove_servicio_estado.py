# Generated by Django 5.0.6 on 2024-07-09 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mikrotik", "0014_servicio_segmentoip"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="servicio",
            name="estado",
        ),
    ]