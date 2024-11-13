from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')


def notSignedIn(request):
    #return render(request, 'notSignedIn.html')

    return ("HELLLO")
def signedIn(request):
    return render(request, 'signedIn.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def viewTest(request):
    return HttpResponse("hello world!")

