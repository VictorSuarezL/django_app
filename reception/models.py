from django.db import models


# Create your models here.
class Reception(models.Model):
    car = models.OneToOneField("catalog.Car", on_delete=models.CASCADE, default=None)
    f_reception = models.DateTimeField(blank=True, null=True)
    n_recepcion = models.TextField(blank=True, null=True)
    recepcionador = models.CharField(max_length=100, blank=True, null=True)
    granizo = models.BooleanField(default=False)
    bollos = models.BooleanField(default=False)
    cristales = models.BooleanField(default=False)
    bandeja = models.BooleanField(default=False)
    faros_pilotos = models.BooleanField(default=False)
    son_motor = models.BooleanField(default=False)
    embrague = models.BooleanField(default=False)
    testigos = models.BooleanField(default=False)
    pantalla = models.BooleanField(default=False)
    quemaduras = models.BooleanField(default=False)
    tarjeta_sd = models.BooleanField(default=False)
    doble_llave = models.TextField(blank=True, null=True)
    notas_doble_llave = models.TextField(blank=True, null=True)
    proveedor = models.CharField(max_length=100, blank=True, null=True)
    info_transporte = models.TextField(blank=True, null=True)
    nota_transporte = models.TextField(blank=True, null=True)
