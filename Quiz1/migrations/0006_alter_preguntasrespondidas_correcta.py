# Generated by Django 3.2.6 on 2021-08-28 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz1', '0005_auto_20210820_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preguntasrespondidas',
            name='correcta',
            field=models.BooleanField(default=False, verbose_name='¿Es esta la respuesta correcta?'),
        ),
    ]
