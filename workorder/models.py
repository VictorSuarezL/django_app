from django.db import models

# Create your models here.
class WorkOrder(models.Model):
    car = models.OneToOneField("catalog.Car", on_delete=models.CASCADE)
    aceite_litros = models.DecimalField(
        max_digits=2, decimal_places=2, blank=True, null=True
    )
    aceite_tipo = models.CharField(max_length=100, blank=True, null=True)
    aceite_pedir = models.BooleanField(default=False)
    aceite_cambio = models.BooleanField(default=False)
    neumaticos_numero = models.IntegerField(blank=True, null=True)
    neumaticos_medidas = models.CharField(max_length=100, blank=True, null=True)
    bateria = models.TextField(blank=True, null=True)
    otros_recambios = models.TextField(blank=True, null=True)
    otras_tareas = models.TextField(blank=True, null=True)
    filtro_aceite = models.BooleanField(default=False)
    filtro_aire = models.BooleanField(default=False)
    filtro_hab = models.BooleanField(default=False)
    distribucion = models.BooleanField(default=False)
    escobilla_del = models.BooleanField(default=False)
    escobilla_tras = models.BooleanField(default=False)
    pastillas_del = models.BooleanField(default=False)
    pastillas_tras = models.BooleanField(default=False)
    liquido_frenos = models.BooleanField(default=False)
