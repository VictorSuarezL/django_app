from django.urls import path, re_path
from . import views
from .views import BrandAutocomplete

urlpatterns = [
    path('', views.catalog_list, name='catalog_list'),
    path('edit/<int:id>/', views.edit_car, name='edit_car'),
    path('add/', views.add_car, name='add_car'),
    path('search/', views.search_cars, name='search_cars'),
    path('delete/<int:id>/', views.delete_car, name='delete_car'),
    re_path(r'^brand-autocomplete/$', BrandAutocomplete.as_view(), name='brand-autocomplete'),
]
