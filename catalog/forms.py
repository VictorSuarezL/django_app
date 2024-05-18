from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['matricula', 'chassis', 'registration_date',  'registration_date', 'documented']
        labels = {
            'matricula': 'Matrícula',
            'chassis': 'Chasis',
            'registration_date': 'Fecha de Registro',
            'documented': 'Documentado',
        }
        widgets = {
            'matricula': forms.TextInput(attrs={'class': '"form-control-sm"'}),
            'chassis': forms.TextInput(attrs={'class': '"form-control-sm"'}),
            'registration_date': forms.DateInput(attrs={'class': '"form-control-sm"'}),
            'documented': forms.CheckboxInput(attrs={'class': '"form-control-sm"'}),
        }
    # def clean(self):
    #     cleaned_data = super().clean()
    #     matricula = cleaned_data.get('matricula')
    #     chassis = cleaned_data.get('chassis')
    #     if matricula == chassis:
    #         raise forms.ValidationError('La matrícula no puede ser igual al chasis')
    #     return cleaned_data