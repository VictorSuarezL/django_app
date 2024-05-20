from django import forms
from .models import Car
from datetime import date


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            "matricula",
            "chassis",
            "registration_date",
            "documented",
            "brand",
            "color",
            "buy_price",
            "sale_price",
            "km",
            "fuel",
            "transmission",
            "version",
            "car_model"
        ]
        labels = {
            "matricula": "Matrícula",
            "chassis": "Chasis",
            "registration_date": "Fecha de Matriculación",
            "documented": "Documentado",
            "brand": "Marca",
            "color": "Color",
            "buy_price": "Precio de Compra",
            "sale_price": "Precio de Venta",
            "km": "Kilometraje",
            "fuel": "Combustible",
            "transmission": "Transmisión",
            "version": "Versión",
            "car_model": "Modelo",
        }
        widgets = {
            "matricula": forms.TextInput(),
            "chassis": forms.TextInput(),
            "registration_date": forms.DateInput(attrs={"type": "date"}),
            "documented": forms.CheckboxInput(),
            "brand": forms.Select(),
            "color": forms.TextInput(),
            "buy_price": forms.NumberInput(),
            "sale_price": forms.NumberInput(),
            "km": forms.NumberInput(),
            "fuel": forms.TextInput(),
            "transmission": forms.TextInput(),
            "version": forms.TextInput(),
            "car_model": forms.TextInput(),
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
                "La fecha de matriculación debe ser anterior a la fecha actual.",
            )

        # Validación de documento
        documented = cleaned_data.get("documented")
        if documented is False:
            self.add_error(
                "documented",
                "Debes asegurarte de subir la documentación antes de proceder.",
            )

        # Validación de marca
        brand = cleaned_data.get("brand")
        if brand is None:
            self.add_error("brand", "Este campo es obligatorio.")
        
        # Validación de color
        color = cleaned_data.get("color")
        if not color:
            self.add_error("color", "Este campo es obligatorio.")
        
        # Validación de buy_price
        buy_price = cleaned_data.get("buy_price")
        if buy_price is None:
            self.add_error("buy_price", "Este campo es obligatorio.")
        elif buy_price <= 0:
            self.add_error("buy_price", "El precio de compra debe ser mayor a 0.")
        
        # Validación de sale_price
        sale_price = cleaned_data.get("sale_price")
        if sale_price is None:
            self.add_error("sale_price", "Este campo es obligatorio.")
        elif sale_price <= 0:
            self.add_error("sale_price", "El precio de venta debe ser mayor a 0.")
        
        # Validación de km
        km = cleaned_data.get("km")
        if km is None:
            self.add_error("km", "Este campo es obligatorio.")
        elif km <= 0:
            self.add_error("km", "El kilometraje debe ser mayor a 0.")
        
        # Validación de fuel
        fuel = cleaned_data.get("fuel")
        if not fuel:
            self.add_error("fuel", "Este campo es obligatorio.")
            
        # Validación de transmission
        transmission = cleaned_data.get("transmission")
        if not transmission:
            self.add_error("transmission", "Este campo es obligatorio.")
        
        # Validación de version
        version = cleaned_data.get("version")
        if not version:
            self.add_error("version", "Este campo es obligatorio.")
        
        # Validación de car_model
        car_model = cleaned_data.get("car_model")
        if not car_model:
            self.add_error("car_model", "Este campo es obligatorio.")


class CarSearchForm(forms.Form):
    matricula = forms.CharField(max_length=80, required=False)
    chassis = forms.CharField(max_length=30, required=False)
    registration_date = forms.DateField(required=False)


class CarEditForm(CarForm):
    pass
