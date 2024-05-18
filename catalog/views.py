from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def catalog_list(request):
    # return HttpResponse("Your are here!")
    return render(request, 'catalog/catalog_list.html', {})