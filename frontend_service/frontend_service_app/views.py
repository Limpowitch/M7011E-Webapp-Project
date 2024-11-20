from django.shortcuts import render
import requests

RECIPE_SERVICE_URL = 'http://localhost:8001'

# Create your views here.
def homepage(request):
    limit = 4
    response = requests.get(f'{RECIPE_SERVICE_URL}/recipes/', params={'limit': limit})
    recipes = response.json()
    return render(request, 'homepage.html', {'recipes': recipes})

def recipe_list(request):
    response = requests.get(f'{RECIPE_SERVICE_URL}/recipes/')
    recipes = response.json()
    return render(request, 'recipe_list.html', {'recipes': recipes})