from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name

class CarManager(models.Manager):
    def search(self, matricula=None, chassis=None, registration_date=None, documented=None):
        queryset = self.get_queryset()

        if matricula:
            queryset = queryset.filter(matricula__icontains=matricula)
        if chassis:
            queryset = queryset.filter(chassis__icontains=chassis)
        if registration_date:
            queryset = queryset.filter(registration_date=registration_date)
        
        return queryset
    
class Car(models.Model):

    matricula = models.CharField(max_length=80, unique=True, blank=False, null=False)
    chassis = models.CharField(max_length=30, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    registration_date = models.DateField(blank=False, null=False)
    documented = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=False, null=False)
    
    objects = CarManager()

    def __str__(self):
        return f"{self.matricula} - {self.brand}"