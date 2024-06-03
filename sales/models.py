from django.db import models
from catalog.models import Car


class Province(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name


class Municipality(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE, blank=False, null=False
    )

    def __str__(self):
        return self.name


class Client(models.Model):
    nombre_cliente = models.CharField(max_length=100, blank=False, null=False)
    dni = models.CharField(max_length=15, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    telefono_nombre = models.CharField(max_length=100, blank=True, null=True)
    telefono_2 = models.CharField(max_length=15, blank=True, null=True)
    telefono_2_nombre = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    provincia = models.ForeignKey(
        Province, on_delete=models.CASCADE, blank=True, null=True
    )
    localidad = models.ForeignKey(
        Municipality, on_delete=models.CASCADE, blank=True, null=True
    )
    direccion = models.CharField(max_length=100, blank=True, null=True)
    cp = models.IntegerField(blank=True, null=True)
    empresa = models.BooleanField(default=False)
    e_nombre = models.CharField(max_length=100, blank=True, null=True)
    e_dni = models.CharField(max_length=15, blank=True, null=True)
    

    def __str__(self):
        return self.name


class Sale(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    guarantee = models.BooleanField(default=False)
    equipment_a = models.CharField(max_length=100, blank=True, null=True)
    equipment_b = models.CharField(max_length=100, blank=True, null=True)
