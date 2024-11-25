from django.shortcuts import render
import requests, random
from .forms import RecipeForm

RECIPE_SERVICE_URL = 'http://localhost:8001'

# Create your views here.
def homepage(request):
    limit = 4
    
    response = requests.get(f'{RECIPE_SERVICE_URL}/recipes/', params={'limit': limit})
    recipes = response.json()
    return render(request, 'homepage.html', {'recipes': recipes})

def category(request, category):
    response = requests.get(f'{RECIPE_SERVICE_URL}/category/{category}/')
    recipes = response.json()
    return render(request, 'category.html', {'recipes': recipes})

# def recipe_list(request):
#     response = requests.get(f'{RECIPE_SERVICE_URL}/recipes/')
#     recipes = response.json()
#     return render(request, 'recipe_list.html', {'recipes': recipes})

def recipe_detail(request, id):
    response = requests.get(f'{RECIPE_SERVICE_URL}/recipes/{id}/')
    recipe = response.json()
    return render(request, 'recipe.html', {'recipe': recipe})

def recipe_create(request):
    return render(request, 'recipe_create.html')


def upload_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            try:
                # Send the form data to the backend
                data = form.cleaned_data
                files = {'image': request.FILES['image']}
                response = requests.post(f'{RECIPE_SERVICE_URL}/recipes/create/', data=data, files=files)
                if response.status_code == 201:
                    return redirect('homepage')  # Redirect to homepage on success
                else:
                    error = response.json().get('error', 'Failed to create recipe.')
            except requests.exceptions.RequestException as e:
                error = f"Error communicating with the backend: {e}"
            # Render the form with the error message
            return render(request, 'recipe_create.html', {'form': form, 'error': error})
    else:
        form = RecipeForm()

    return render(request, 'recipe_create.html', {'form': form})
