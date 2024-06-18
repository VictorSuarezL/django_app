from django import forms
from .models import Reception
from sales.forms import CustomDateInput


class ReceptionForm(forms.ModelForm):
    class Meta:
        model = Reception
        fields = '__all__'
        widgets = {
            'f_reception': CustomDateInput(),
            'f_delivery': CustomDateInput(),
        }
