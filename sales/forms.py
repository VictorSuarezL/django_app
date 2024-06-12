
from dal import autocomplete
from django import forms
from .models import Sales

class CustomDateInput(forms.DateInput):
    input_type = 'date'

    def format_value(self, value):
        if isinstance(value, str):
            return value
        if value is None:
            return ''
        return value.strftime('%Y-%m-%d')

class SalesForm(forms.ModelForm):
    vendedor = forms.CharField(
        widget=autocomplete.ListSelect2(attrs={"data-theme": "bootstrap-5", "style": "width: 100%;"}, 
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
        
