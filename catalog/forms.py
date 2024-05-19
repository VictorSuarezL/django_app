from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['matricula']
        labels = {
            'matricula': 'Matrícula',
        }
        widgets = {
            'matricula': forms.TextInput(),
        }
        def clean(self):
            cleaned_data = super().clean()
            matricula = cleaned_data.get('matricula')
            if Car.objects.filter(matricula=matricula).exists():
                raise forms.ValidationError("La matrícula ya existe.")
            return cleaned_data
        # fields = ['matricula', 'chassis', 'registration_date',  'registration_date', 'documented']
        # labels = {
        #     'matricula': 'Matrícula',
        #     'chassis': 'Chasis',
        #     'registration_date': 'Fecha de Registro',
        #     'documented': 'Documentado',
        # }
        # widgets = {
        #     'matricula': forms.TextInput(attrs={'class': '"form-control-sm"'}),
        #     'chassis': forms.TextInput(attrs={'class': '"form-control-sm"'}),
        #     'registration_date': forms.DateInput(attrs={'type': 'date', 'class': '"form-control-sm"'}),
        #     'documented': forms.CheckboxInput(attrs={'class': '"form-control-sm"'}),
        # }
    # def clean(self):
    #     cleaned_data = super().clean()
        
    #     matricula = self.cleaned_data.get('matricula')
    #     if Car.objects.filter(matricula=matricula).exists():
    #         raise forms.ValidationError("La matrícula ya existe.")
    #     return cleaned_data
    # def clean(self):
    #     cleaned_data = super().clean()
    #     matricula = cleaned_data.get('matricula')
    #     chassis = cleaned_data.get('chassis')
    #     if matricula == chassis:
    #         raise forms.ValidationError('La matrícula no puede ser igual al chasis')
    #     return cleaned_data

class CarSearchForm(forms.Form):
    matricula = forms.CharField(max_length=80, required=False)
    chassis = forms.CharField(max_length=30, required=False)
    registration_date = forms.DateField(required=False)
    
class CarEditForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['matricula', 'chassis', 'registration_date', 'documented']