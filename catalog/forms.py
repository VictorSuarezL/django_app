from django import forms
from .models import Car
from datetime import date


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            "matricula",
            "chasis",
            "f_matriculacion",
            "documented",
            "marca",
            "color",
            # "buy_price",
            # "sale_price",
            "km",
            "combustible",
            "cambio",
            "version",
            "modelo",
        ]
        labels = {
            "matricula": "Matrícula",
            "chasis": "Chasis",
            "f_matriculacion": "Fecha de Matriculación",
            "documented": "Documentado",
            "marca": "Marca",
            "color": "Color",
            # "buy_price": "Precio de Compra",
            # "sale_price": "Precio de Venta",
            "km": "Kilometraje",
            "combustible": "Combustible",
            "cambio": "Transmisión",
            "version": "Versión",
            "modelo": "Modelo",
        }
        widgets = {
            "matricula": forms.TextInput(),
            "chasis": forms.TextInput(),
            "f_matriculacion": forms.DateInput(attrs={"type": "date"}),
            "documented": forms.CheckboxInput(),
            "marca": forms.Select(),
            "color": forms.TextInput(),
            # "buy_price": forms.NumberInput(),
            # "sale_price": forms.NumberInput(),
            "km": forms.NumberInput(),
            "combustible": forms.TextInput(),
            "cambio": forms.TextInput(),
            "version": forms.TextInput(),
            "modelo": forms.TextInput(),
        }

    def clean(self):
        cleaned_data = super().clean()

        # Validación de matricula
        matricula = cleaned_data.get("matricula")
        if not matricula:
            self.add_error("matricula", "Este campo es obligatorio.")

        # Validación de chasis
        chasis = cleaned_data.get("chasis")
        if not chasis:
            self.add_error("chasis", "Este campo es obligatorio.")

        # Validación de f_matriculacion
        f_matriculacion = cleaned_data.get("f_matriculacion")
        if f_matriculacion is None:
            self.add_error("f_matriculacion", "Este campo es obligatorio.")
        elif f_matriculacion >= date.today():
            self.add_error(
                "f_matriculacion",
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
        marca = cleaned_data.get("marca")
        if marca is None:
            self.add_error("marca", "Este campo es obligatorio.")

        # Validación de color
        color = cleaned_data.get("color")
        if not color:
            self.add_error("color", "Este campo es obligatorio.")

        # # Validación de buy_price
        # buy_price = cleaned_data.get("buy_price")
        # if buy_price is None:
        #     self.add_error("buy_price", "Este campo es obligatorio.")
        # elif buy_price <= 0:
        #     self.add_error("buy_price", "El precio de compra debe ser mayor a 0.")

        # # Validación de sale_price
        # sale_price = cleaned_data.get("sale_price")
        # if sale_price is None:
        #     self.add_error("sale_price", "Este campo es obligatorio.")
        # elif sale_price <= 0:
        #     self.add_error("sale_price", "El precio de venta debe ser mayor a 0.")

        # Validación de km
        km = cleaned_data.get("km")
        if km is None:
            self.add_error("km", "Este campo es obligatorio.")
        elif km <= 0:
            self.add_error("km", "El kilometraje debe ser mayor a 0.")

        # Validación de combustible
        combustible = cleaned_data.get("combustible")
        if not combustible:
            self.add_error("combustible", "Este campo es obligatorio.")

        # Validación de cambio
        cambio = cleaned_data.get("cambio")
        if not cambio:
            self.add_error("cambio", "Este campo es obligatorio.")

        # Validación de version
        version = cleaned_data.get("version")
        if not version:
            self.add_error("version", "Este campo es obligatorio.")

        # Validación de modelo
        modelo = cleaned_data.get("modelo")
        if not modelo:
            self.add_error("modelo", "Este campo es obligatorio.")


class CarSearchForm(forms.Form):
    matricula = forms.CharField(max_length=80, required=False)
    chasis = forms.CharField(max_length=30, required=False)
    f_matriculacion = forms.DateField(required=False)


class CarEditForm(CarForm):
    pass
