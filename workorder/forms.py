from django import forms
from workorder.models import WorkOrder

class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = "__all__"
        widgets = {
            'car': forms.HiddenInput(),
        }
