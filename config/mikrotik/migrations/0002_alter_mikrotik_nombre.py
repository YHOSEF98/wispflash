# Generated by Django 4.2.5 on 2023-09-20 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mikrotik", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mikrotik",
            name="nombre",
            field=models.CharField(max_length=50, unique=True, verbose_name="Nombre"),
        ),
    ]
