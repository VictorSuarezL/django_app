# Generated by Django 5.0.6 on 2024-05-20 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_car_buy_price_car_color_car_fuel_car_km_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='car_model',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]