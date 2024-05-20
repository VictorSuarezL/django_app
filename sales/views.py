from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to the Sales app!")# Create your views here.
