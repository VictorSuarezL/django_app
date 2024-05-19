from django.db import models

# Create your models here.

class CarManager(models.Manager):
    def search(self, matricula=None, chassis=None, registration_date=None, documented=None):
        queryset = self.get_queryset()

        if matricula:
            queryset = queryset.filter(matricula__icontains=matricula)
        if chassis:
            queryset = queryset.filter(chassis__icontains=chassis)
        if registration_date:
            queryset = queryset.filter(registration_date=registration_date)
        if documented is not None:
            queryset = queryset.filter(documented=documented)
        
        return queryset
    
class Car(models.Model):

    matricula = models.CharField(max_length=80, unique=True)
    chassis = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    registration_date = models.DateField(null=True)
    documented = models.BooleanField(default=False)
    
    objects = CarManager()
