from django.urls import path

from reception.views import ReceptionView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reception/', ReceptionView.as_view(), name='reception'),
    path('reception/<int:car_id>/', ReceptionView.as_view(), name='reception_detail'),
    
    
]
