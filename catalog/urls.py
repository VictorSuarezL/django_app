from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog_list, name='catalog_list'),
    path('car/<int:id>/', views.car_detail, name='car_detail'),
    path('car/new/', views.car_new, name='car_new'),
]