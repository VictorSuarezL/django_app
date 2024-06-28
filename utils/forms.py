from django import forms

class CustomDateInput(forms.DateInput):
    input_type = 'date'

    def format_value(self, value):
        if isinstance(value, str):
            return value
        if value is None:
            return ''
        return value.strftime('%Y-%m-%d')

