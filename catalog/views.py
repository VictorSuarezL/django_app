from django.http import HttpResponse
from django.shortcuts import render, redirect
from catalog.models import Car
from catalog.forms import CarForm
# Create your views here.
def catalog_list(request):
    # return HttpResponse("Your are here!")
    cars=Car.objects.all()
    return render(request, 'catalog/catalog_list.html', {'cars': cars})

def car_detail(request, id):
    car = Car.objects.get(id=id)
    return render(request, 'catalog/car_detail.html', {'car': car})

def car_new(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save()
            return redirect('car_detail', id=car.id)
    form = CarForm()
    return render(request, 'catalog/car_form.html', {'form': form}) 