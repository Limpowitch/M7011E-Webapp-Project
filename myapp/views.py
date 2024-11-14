from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def viewTest(request):
    return HttpResponse("hello world!")

def index(request):
    return render(request, "index.html")