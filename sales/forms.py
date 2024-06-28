
from dal import autocomplete
from django import forms
from .models import Sales
from utils.forms import CustomDateInput

# class CustomDateInput(forms.DateInput):
#     input_type = 'date'

#     def format_value(self, value):
#         if isinstance(value, str):
#             return value
#         if value is None:
#             return ''
#         return value.strftime('%Y-%m-%d')

def get_choice_list():
    return [
        "Álvaro",
        "Carlos M",
        "David",
        "Javier",
        "Joel",
        "Juan",
        "Juan José",
        "Martín",
        "Miguel",
        "Salvador",
        "Sandra"
        ]

class SalesForm(forms.ModelForm):
    vendedor = autocomplete.Select2ListChoiceField(
        choice_list=get_choice_list,
        widget=autocomplete.ListSelect2(attrs={"data-theme": "bootstrap-5"}, 
                                        url='custom-list-autocomplete'),
        required=False
    )
    f_venta = forms.DateField(widget=CustomDateInput(), required=False) 
    garantia_fab_fecha = forms.DateField(widget=CustomDateInput(), required=False)
    fecha_entrega = forms.DateField(widget=CustomDateInput(), required=False)
    hora_entrega = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}), required=False)
        
    
    class Meta:
        model = Sales
        fields = "__all__"
        # widgets = {
        #     'car': forms.HiddenInput(),
        # }
        
