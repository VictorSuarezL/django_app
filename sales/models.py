
from django.db import models
from catalog.models import Car  # Asegúrate de que la importación sea correcta

class Province(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    
    def __str__(self):
        return self.name

class Municipality(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, blank=False, null=False)
    
    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    dni = models.CharField(max_length=15, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    phone2 = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, blank=True, null=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, blank=True, null=True)
    postal_code = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name

class Sale(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    guarantee = models.BooleanField(default=False)
    equipment_a = models.CharField(max_length=100, blank=True, null=True)
    equipment_b = models.CharField(max_length=100, blank=True, null=True)
    
    