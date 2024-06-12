from django.urls import path
from . import views
from sales.views import SalerListAutocomplete, SalesView

urlpatterns = [
    path('', views.index, name='index'),
    path('sales/', SalesView.as_view(), name='sales'),
    # path('sales/<int:id>/', views.SalesView.as_view(), name='sale_detail'),
    path('sales/<int:car_id>/', SalesView.as_view(), name='sale_detail'),
    path('custom-list-autocomplete/', SalerListAutocomplete.as_view(), name='custom-list-autocomplete'),
    # path('sales/edit/<int:pk>/', SaleUpdateView.as_view(), name='sale_edit'),
    # path('sales/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
]
