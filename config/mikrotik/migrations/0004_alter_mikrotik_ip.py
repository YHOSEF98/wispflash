# Generated by Django 4.2.5 on 2023-09-22 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mikrotik", "0003_mikrotik_puertoapissl_mikrotik_puertossh_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mikrotik",
            name="ip",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
