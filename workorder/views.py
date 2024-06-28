
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from workorder.models import WorkOrder
from workorder.forms import WorkOrderForm
from catalog.forms import CarSearchForm
from catalog.models import Car
from django.shortcuts import render, get_object_or_404
from utils.views import BaseView

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the workorder index.")

class WorkOrderView(BaseView):
    model = WorkOrder
    form_class = WorkOrderForm
    template_name = 'reception/reception_form.html'
    search_form_class = CarSearchForm
    search_model = Car
    url_show_all_button = 'workorder'
    url_show_all_button_detail = 'workorder_detail'

