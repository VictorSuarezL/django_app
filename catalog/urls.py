from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog_list, name='catalog_list'),
    path('edit/<int:id>/', views.edit_car, name='edit_car'),
    path('add/', views.add_car, name='add_car'),
    path('search/', views.search_cars, name='search_cars'),
    path('delete/<int:id>/', views.delete_car, name='delete_car'),
]