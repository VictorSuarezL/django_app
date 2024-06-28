from django.urls import path
from . import views
# from sales.views import SalerListAutocomplete, SalesView
from workorder.views import WorkOrderView

urlpatterns = [
    path('', views.index, name='index'),
    path('workorder/', WorkOrderView.as_view(), name='workorder'),
    path('workorder/<int:car_id>/', WorkOrderView.as_view(), name='workorder_detail'),
    # path('sales/<int:car_id>/', SalesView.as_view(), name='sale_detail'),
    # path('custom-list-autocomplete/', SalerListAutocomplete.as_view(), name='custom-list-autocomplete'),
    # path('sales/edit/<int:pk>/', SaleUpdateView.as_view(), name='sale_edit'),
    # path('sales/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
]
