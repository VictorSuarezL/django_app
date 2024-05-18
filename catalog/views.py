from django.http import HttpResponse
from django.shortcuts import render
from catalog.models import Car
# Create your views here.
def catalog_list(request):
    # return HttpResponse("Your are here!")
    cars=Car.objects.all()
    return render(request, 'catalog/catalog_list.html', {'cars': cars})

def car_detail(request, id):
    car = Car.objects.get(id=id)
    return render(request, 'catalog/car_detail.html', {'car': car})