# Generated by Django 5.0.6 on 2024-06-08 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='f_compra',
            field=models.DateField(blank=True, default='1900-01-01', null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='f_matriculacion',
            field=models.DateField(default='1900-01-01'),
        ),
        migrations.AlterField(
            model_name='car',
            name='f_prox_itv',
            field=models.DateField(blank=True, default='1900-01-01', null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='f_ultima_itv',
            field=models.DateField(blank=True, default='1900-01-01', null=True),
        ),
    ]
