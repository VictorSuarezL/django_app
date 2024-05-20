from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Car
from catalog.forms import CarForm, CarSearchForm, CarEditForm


def add_car(request):
    cars = Car.objects.all()
    search_form = CarSearchForm(request.GET or None)
    form = CarForm()
    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add_car")
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
        "catalog/add_car.html",
        {
            "form": form,
            "cars": cars,
            "search_form": search_form,
        },
    )


def edit_car(request, id):
    car = get_object_or_404(Car, id=id)
    car.registration_date = car.registration_date.strftime('%Y-%m-%d')
    form = CarEditForm(instance=car)
    search_form = CarSearchForm(request.GET or None)
    cars = Car.objects.all()

    if request.method == "GET" and search_form.is_valid():
        cars = Car.objects.search(
            matricula=search_form.cleaned_data.get("matricula"),
            chassis=search_form.cleaned_data.get("chassis"),
            registration_date=search_form.cleaned_data.get("registration_date"),
        )
        return render(
            request,
            "catalog/edit_car.html",
            {
                "car": car,
                "form": form,
                "cars": cars,
                "search_form": search_form,
            },
        )

    elif request.method == "POST":
        form = CarEditForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect("add_car")

    return render(
        request,
        "catalog/edit_car.html",
        {
            "car": car,
            "form": form,
            "cars": cars,
            "search_form": search_form,
        },
    )


def delete_car(request, id):
    car = get_object_or_404(Car, id=id)
    if request.method == "POST":
        car.delete()
        return redirect(
            "add_car"
        )  
    return render(request, "catalog/confirm_delete.html", {"car": car})


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

def catalog_list(request):
    # return HttpResponse("Your are here!")
    cars = Car.objects.all()
    return render(request, "catalog/catalog_list.html", {"cars": cars})
