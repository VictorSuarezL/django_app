from django.db import models

# Create your models here.
class Car(models.Model):

    matricula = models.CharField(max_length=80, unique=True)
    chassis = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    registration_date = models.DateField(null=True)
    documented = models.BooleanField(default=False)
