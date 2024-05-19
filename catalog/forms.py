from django import forms
from .models import Car
from datetime import date


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["matricula", "chassis", "registration_date", "documented"]
        labels = {
            "matricula": "Matrícula",
            "chassis": "Chasis",
            "registration_date": "Fecha de Registro",
            "documented": "Documentado",
        }
        widgets = {
            "matricula": forms.TextInput(),
            "chassis": forms.TextInput(),
            "registration_date": forms.DateInput(attrs={"type": "date"}),
            "documented": forms.CheckboxInput(),
        }

    def clean(self):
        cleaned_data = super().clean()

        # Validación de matricula
        matricula = cleaned_data.get("matricula")
        if not matricula:
            self.add_error("matricula", "Este campo es obligatorio.")

        # Validación de chassis
        chassis = cleaned_data.get("chassis")
        if not chassis:
            self.add_error("chassis", "Este campo es obligatorio.")

        # Validación de registration_date
        registration_date = cleaned_data.get("registration_date")
        if registration_date is None:
            self.add_error("registration_date", "Este campo es obligatorio.")
        elif registration_date >= date.today():
            self.add_error(
                "registration_date",
                "La fecha de registro debe ser anterior a la fecha actual.",
            )
        
        # Validación de documento
        documented = cleaned_data.get("documented")
        if documented is False:
            self.add_error("documented", "Debes asegurarte de subir la documentación antes de proceder.")

    # def clean_registration_date(self):
    #     registration_date = self.cleaned_data.get('registration_date')
    #     if registration_date and registration_date >= date.today():
    #         raise forms.ValidationError("La fecha de registro debe ser anterior a la fecha actual.")
    #     return registration_date
    # def clean(self):
    #     cleaned_data = super().clean()
    #     matricula = cleaned_data.get('matricula')
    #     chassis = cleaned_data.get('chassis')
    #     if matricula == chassis:
    #         raise forms.ValidationError('La matrícula no puede ser igual al chasis')
    #     return cleaned_data
    # def clean(self):
    #     cleaned_data = super().clean()
    #     matricula = cleaned_data.get('matricula')
    #     if Car.objects.filter(matricula=matricula).exists():
    #         raise forms.ValidationError("La matrícula ya existe.")
    #     return cleaned_data
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


class CarSearchForm(forms.Form):
    matricula = forms.CharField(max_length=80, required=False)
    chassis = forms.CharField(max_length=30, required=False)
    registration_date = forms.DateField(required=False)


class CarEditForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["matricula", "chassis", "registration_date"]
