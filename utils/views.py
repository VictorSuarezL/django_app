
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.forms import ModelForm

class BaseView(View):
    model = None
    form_class = None
    template_name = None
    search_form_class = None
    search_model = None
    related_field_name = None
    url_show_all_button = None
    url_show_all_button_detail = None
    
    def get(self, request, car_id=None):
        search_form, objects = self.get_search_form(request)

        if car_id:
            car = get_object_or_404(self.search_model, id=car_id)
            obj, created = self.model.objects.get_or_create(car=car)
            obj_form = self.form_class(instance=obj)
        else:
            obj_form = self.form_class()

        context = {
            'search_form': search_form,
            'form': obj_form,
            'cars': objects,
            'car': car if car_id else None,
            'car_id': car_id,
            'url_show_all_button': self.url_show_all_button,
            'url_show_all_button_detail': self.url_show_all_button_detail
        }

        return render(request, self.template_name, context)


    def post(self, request, car_id=None):
        search_form, objects = self.get_search_form(request)

        car = get_object_or_404(self.search_model, id=car_id)
        try:
            obj = getattr(car, self.related_field_name)
            obj_form = self.form_class(request.POST, instance=obj)
        except self.model.DoesNotExist:
            obj_form = self.form_class(request.POST)

        if obj_form.is_valid():
            obj = obj_form.save(commit=False)
            setattr(obj, self.related_field_name, car)
            obj.save()
            # return redirect(self.url_show_all_button)

        context = {
            'search_form': search_form,
            'form': obj_form,
            'cars': objects,
            'car_id': car_id,
            'url_show_all_button': self.url_show_all_button,
            'url_show_all_button_detail': self.url_show_all_button_detail
        }

        return render(request, self.template_name, context)

    def get_search_form(self, request):
        search_form = self.search_form_class(request.GET or None)
        if search_form.is_valid():
            objects = self.search_model.objects.search(
                matricula=search_form.cleaned_data.get("matricula"),
                chasis=search_form.cleaned_data.get("chasis"),
                f_matriculacion=search_form.cleaned_data.get("f_matriculacion"),
                stock=search_form.cleaned_data.get("stock")
            )
        else:
            objects = self.search_model.objects.all()
        return search_form, objects

