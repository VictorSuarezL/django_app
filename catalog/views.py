from pyexpat.errors import messages
from sqlite3 import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Car
from catalog.forms import CarForm, CarSearchForm, CarEditForm


# Create your views here.
def catalog_list(request):
    # return HttpResponse("Your are here!")
    cars = Car.objects.all()
    return render(request, "catalog/catalog_list.html", {"cars": cars})


def car_detail(request, id):
    car = get_object_or_404(Car, id=id)
    form = CarForm(instance=car)
    cars = Car.objects.all()
    if request.method == "POST":
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
        return redirect("car_new") 
    return render(request, "catalog/car_detail.html", {"car": car,
                                                       "form": form,
                                                       "cars": cars})

# def edit_car(request, id):
#     car = get_object_or_404(Car, id=id)
#     if request.method == 'POST':
#         form = CarEditForm(request.POST, instance=car)
#         if form.is_valid():
#             form.save()
#             return redirect('search_cars')  # Redirige a la vista de búsqueda después de editar
#     else:
#         form = CarEditForm(instance=car)
#     return render(request, 'catalog/edit_car.html', {'form': form, 'car': car})

def delete_car(request, id):
    car = get_object_or_404(Car, id=id)
    if request.method == 'POST':
        car.delete()
        return redirect('car_new')  # Redirige a la vista de búsqueda después de eliminar
    return render(request, 'catalog/confirm_delete.html', {'car': car})

def car_new(request):
    cars = Car.objects.all()
    search_form = CarSearchForm(request.GET or None)
    form = CarForm()
    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("car_new")
    elif search_form.is_valid():
        cars = Car.objects.search(
            matricula=search_form.cleaned_data.get("matricula"),
            chassis=search_form.cleaned_data.get("chassis"),
            registration_date=search_form.cleaned_data.get("registration_date"),
        )
    else:
        form = CarForm()
    return render(
        request,
        "catalog/car_form.html",
        {
            "form": form,
            "cars": cars,
            "search_form": search_form,
        },
    )


def search_cars(request):
    search_form = CarSearchForm(request.GET or None)
    cars = Car.objects.all()
    if search_form.is_valid():

        cars = Car.objects.search(
            matricula=search_form.cleaned_data.get("matricula"),
            chassis=search_form.cleaned_data.get("chassis"),
            registration_date=search_form.cleaned_data.get("registration_date"),
        )
    return render(
        request, "catalog/search_cars.html", {"cars": cars, "search_form": search_form}
    )
