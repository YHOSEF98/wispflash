# Generated by Django 4.2.5 on 2023-09-22 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mikrotik", "0002_alter_mikrotik_nombre"),
    ]

    operations = [
        migrations.AddField(
            model_name="mikrotik",
            name="puertoapissl",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="mikrotik",
            name="puertossh",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="mikrotik",
            name="puertotelnet",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
