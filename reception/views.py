from django.http import HttpResponse
from utils.views import BaseView
from catalog.models import Car
from catalog.forms import CarSearchForm
from reception.forms import ReceptionForm
from reception.models import Reception
from django.shortcuts import render, get_object_or_404


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the reception index.")

class ReceptionView(BaseView):
    model = Reception
    form_class = ReceptionForm
    template_name = 'reception/reception_form.html'
    search_form_class = CarSearchForm
    search_model = Car
    related_field_name = 'reception'
    url_show_all_button = "reception"
    url_show_all_button_detail = "reception_detail"

    # def post(self, request, car_id):
    #     search_form = CarSearchForm(request.GET or None)
        
    #     if search_form.is_valid():
    #         cars = Car.objects.search(
    #             matricula=search_form.cleaned_data.get("matricula"),
    #             chasis=search_form.cleaned_data.get("chasis"),
    #             f_matriculacion=search_form.cleaned_data.get("f_matriculacion"),
    #             stock = search_form.cleaned_data.get("stock")
    #         )
    #     else:
    #         cars = Car.objects.all()
            
    #     car = get_object_or_404(Car, id=car_id)
    #     sales_form = ReceptionForm(request.POST, instance=car)
    #     try:
    #         sale = car.reception
    #         sales_form = ReceptionForm(request.POST, instance=sale)
    #     except Reception.DoesNotExist:
    #         sales_form = ReceptionForm(request.POST)        
        
    #     if sales_form.is_valid():
    #         sale = sales_form.save(commit=False)
    #         sale.car = car
    #         sale.save()

    #     return render(request, 'sales/sales_form.html', {
    #         'search_form': search_form,
    #         'form': sales_form,
    #         'cars': cars,
    #         'car_id': car_id
    #     })
