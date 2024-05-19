from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog_list, name='catalog_list'),
    path('car/<int:id>/', views.edit_car, name='edit_car'),
    path('car/new/', views.car_new, name='car_new'),
    path('search/', views.search_cars, name='search_cars'),
    path('delete/<int:id>/', views.delete_car, name='delete_car'),
]