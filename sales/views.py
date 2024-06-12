from re import search
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from dal import autocomplete
# from requests import get
import sales
from sales.forms import SalesForm
from catalog.forms import CarSearchForm
from catalog.models import Car
from sales.models import Sales

class SalerListAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
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

# class SalesView(View):
#     def get(self, request, car_id=None):
#         search_form = CarSearchForm(request.GET or None)
#         sales_form = SalesForm()
#         # is_editing = False  # Bandera para indicar si estamos en modo de edición

#         if car_id:
#             # is_editing = True
#             # Intenta recuperar la venta para el coche dado
#             try:
#                 sale = Sales.objects.get(car_id=car_id)
#                 sales_form = SalesForm(instance=sale)
#             except Sales.DoesNotExist:
#                 # Si no existe una venta, el formulario sigue vacío
#                 car = get_object_or_404(Car, id=car_id)
#                 sales_form = SalesForm(initial={'car': car})

#         if search_form.is_valid():
#             cars = Car.objects.search(
#                 matricula=search_form.cleaned_data.get("matricula"),
#                 chasis=search_form.cleaned_data.get("chasis"),
#                 f_matriculacion=search_form.cleaned_data.get("f_matriculacion"),
#             )
#         else:
#             cars = Car.objects.all()

#         return render(request, 'sales/sales_form.html', {
#             'search_form': search_form,
#             'form': sales_form,
#             'cars': cars,
#             'car_id': car_id,  # Pasar car_id a la plantilla
#             # 'is_editing': is_editing  # Pasar la bandera de edición a la plantilla
#         })
        
#     def post(self, request, car_id=None):
#         search_form = CarSearchForm(request.GET or None)
#         if car_id:
#             car = get_object_or_404(Car, id=car_id)
#             sale = Sales.objects.filter(car=car).first()
#             if sale:
#                 sales_form = SalesForm(request.POST, instance=sale)
#             else:
#                 sales_form = SalesForm(request.POST)
#                 if sales_form.is_valid():
#                     sale = sales_form.save(commit=False)
#                     sale.car = car
#                     sale.save()
#                     return redirect('index')  # Redirige a una vista que lista todas las ventas
#         else:
#             sales_form = SalesForm(request.POST)
#             if sales_form.is_valid():
#                 sales_form.save()
#                 return redirect('index')

#         if sales_form.is_valid():
#             sales_form.save()
#             return redirect('index')

#         return render(request, 'sales/sales_form.html', {
#             'search_form': search_form, 
#             'form': sales_form,
#             'car_id': car_id
#         })
        
class SalesView(View):
    def get(self, request, car_id=None):
        search_form = CarSearchForm(request.GET or None)

        if search_form.is_valid():
            cars = Car.objects.search(
                matricula=search_form.cleaned_data.get("matricula"),
                chasis=search_form.cleaned_data.get("chasis"),
                f_matriculacion=search_form.cleaned_data.get("f_matriculacion"),
            )
        else:
            cars = Car.objects.all()
        
        if car_id:
            car = get_object_or_404(Car, id=car_id)
            sale = Sales.objects.filter(car=car).first()
            if sale:
                sales_form = SalesForm(instance=sale)
            else:
                sales_form = SalesForm(initial={'car': car})
        else:
            sales_form = SalesForm()

        return render(request, 'sales/sales_form.html', {
            'search_form': search_form,
            'form': sales_form,
            'cars': cars,
            'car_id': car_id
        })

    def post(self, request, car_id=None):
        search_form = CarSearchForm(request.GET or None)
        
        if search_form.is_valid():
            cars = Car.objects.search(
                matricula=search_form.cleaned_data.get("matricula"),
                chasis=search_form.cleaned_data.get("chasis"),
                f_matriculacion=search_form.cleaned_data.get("f_matriculacion"),
            )
        else:
            cars = Car.objects.all()
            
        if car_id:
            car = get_object_or_404(Car, id=car_id)
            sale = Sales.objects.filter(car=car).first()
            if sale:
                sales_form = SalesForm(request.POST, instance=sale)
            else:
                sales_form = SalesForm(request.POST)
                if sales_form.is_valid():
                    sale = sales_form.save(commit=False)
                    sale.car = car
                    sale.save()
        else:
            sales_form = SalesForm(request.POST)
            if sales_form.is_valid():
                sales_form.save()

        if sales_form.is_valid():
            sales_form.save()

        return render(request, 'sales/sales_form.html', {
            'search_form': search_form,
            'form': sales_form,
            'cars': cars,
            'car_id': car_id
        })

def index(request):
    return HttpResponse("Welcome to the Sales app!")# Create your views here.
