# from pyexpat import model
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name

class CarManager(models.Manager):
    def search(self, matricula=None, chasis=None, f_matriculacion=None, documented=None, stock=None):
        queryset = self.get_queryset()

        if matricula:
            queryset = queryset.filter(matricula__icontains=matricula)
        if chasis:
            queryset = queryset.filter(chasis__icontains=chasis)
        if f_matriculacion:
            queryset = queryset.filter(f_matriculacion=f_matriculacion)
        if stock:
            queryset = queryset.filter(stock=stock)
        
        return queryset
    
class Car(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    ubicacion = models.CharField(max_length=50, blank=True, null=True)
    matricula = models.CharField(max_length=80, unique=True, blank=False, null=False)
    stock = models.BooleanField(default=True)
    destino = models.CharField(max_length=50, blank=True, null=True)
    expediente = models.CharField(max_length=80, blank=True, null=True)
    marca = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=False, null=False)
    modelo = models.CharField(max_length=50, blank=True, null=True)
    version = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    f_matriculacion = models.DateField(blank=False, null=False)
    f_compra = models.DateField(blank=True, null=True)
    f_ultima_itv = models.DateField(blank=True, null=True)
    f_prox_itv = models.DateField(blank=True, null=True)
    km = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cambio = models.CharField(max_length=50, blank=True, null=True)
    combustible = models.CharField(max_length=50, blank=True, null=True)
    chasis = models.CharField(max_length=30, blank=False, null=False)
    t_motor = models.CharField(max_length=50, blank=True, null=True)
    c_vehiculo = models.CharField(max_length=50, blank=True, null=True)
    carroceria = models.CharField(max_length=50, blank=True, null=True)
    servi_anterior = models.CharField(max_length=50, blank=True, null=True)
    largo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ancho = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    alto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    consumo_medio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    maletero = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    c_contaminacion = models.CharField(max_length=50, blank=True, null=True)
    client = models.ForeignKey('sales.Client', on_delete=models.SET_NULL, blank=True, null=True)
    documented = models.BooleanField(default=False)
    # sale = models.ForeignKey('sales.Sales', on_delete=models.SET_NULL, blank=True, null=True)
    
    objects = CarManager()

    def __str__(self):
        return f"{self.matricula} - {self.marca}"
