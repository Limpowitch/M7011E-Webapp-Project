from django.shortcuts import render
import requests, random

RECIPE_SERVICE_URL = 'http://localhost:8001'

# Create your views here.
def homepage(request):
    limit = 4
    
    response = requests.get(f'{RECIPE_SERVICE_URL}/recipes/', params={'limit': limit})
    data = response.json()
    recipes = random.sample(data, limit)
    return render(request, 'homepage.html', {'recipes': recipes})

def recipe_list(request):
    response = requests.get(f'{RECIPE_SERVICE_URL}/recipes/')
    recipes = response.json()
    return render(request, 'recipe_list.html', {'recipes': recipes})

def recipe(request):
    limit = 1
    response = requests.get(f'{RECIPE_SERVICE_URL}/recipes/', params={'limit': limit})
    recipe = response.json()
    return render(request, 'recipe.html', {'recipe': recipe})