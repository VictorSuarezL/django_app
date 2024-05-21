from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse


def sales(request):
    return HttpResponse("You are in sales!")# Create your views here.

def index(request):
    return HttpResponse("Welcome to the Sales app!")# Create your views here.
