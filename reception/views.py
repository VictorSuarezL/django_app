from django.http import HttpResponse
from catalog.models import Car
from catalog.forms import CarSearchForm
from reception.forms import ReceptionForm
from reception.models import Reception
from django.views import View
from django.shortcuts import render, get_object_or_404
    

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the reception index.")

class ReceptionView(View):
    model = Reception
    form_class = ReceptionForm
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
            obj = self.model.objects.filter(car=car).first()
            if obj:
                sales_form = self.form_class(instance=obj)
            else:
                sales_form = self.form_class(initial={'car': car})
        else:
            sales_form = self.form_class()

        return render(request, 'reception/reception_form.html', {
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
            obj = self.model.objects.filter(car=car).first()
            if obj:
                sales_form = self.form_class(request.POST, instance=obj)
            else:
                sales_form = self.form_class(request.POST)
                if sales_form.is_valid():
                    obj = sales_form.save(commit=False)
                    obj.car = car
                    obj.save()
        else:
            sales_form = self.form_class(request.POST)
            if sales_form.is_valid():
                sales_form.save()

        # if sales_form.is_valid():
        #     sales_form.save()

        return render(request, 'reception/reception_form.html', {
            'search_form': search_form,
            'form': sales_form,
            'cars': cars,
            'car_id': car_id
        })
