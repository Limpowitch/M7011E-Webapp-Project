from django.shortcuts import render, redirect
from django.contrib import messages
import requests

RECIPE_SERVICE_URL = 'http://localhost:8001'
USER_SERVICE_URL = 'http://localhost:8002'



def homepage(request):
    limit = 4
    
    response = requests.get(f'{RECIPE_SERVICE_URL}/recipes/', params={'limit': limit})
    recipes = response.json()
    return render(request, 'homepage.html', {'recipes': recipes})

def category(request, category):
    response = requests.get(f'{RECIPE_SERVICE_URL}/category/{category}/')
    recipes = response.json()
    return render(request, 'category.html', {'recipes': recipes})

def recipe_detail(request, id):
    response = requests.get(f'{RECIPE_SERVICE_URL}/recipes/{id}/')
    recipe = response.json()
    return render(request, 'recipe.html', {'recipe': recipe})

def create_recipe(request):
    return render(request, 'create_recipe.html')

#Följande funktion är enbart för att visa hur exempelvis man använder JWT authentication mellan services
def get_special_recipes(request):
    access_token = request.session.get('access_token')
    refresh_token = request.session.get('refresh_token')
    next_url = request.GET.get('next', '/')
    if not access_token:
        messages.error(request, 'Please log in to continue.')
        return redirect(next_url)

    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(f'{RECIPE_SERVICE_URL}/specialrecipes/', headers=headers)
    if response.status_code == 200:
        recipes = response.json()
        return render(request, 'create_recipe.html', {'recipes': recipes})
    #Om giltig token skulle expire under använding så prövar vi refresha och skapa en ny token
    elif response.status_code == 401:       
        new_access_token = refresh_token_on_401(refresh_token)
        if new_access_token:
            request.session['access_token'] = new_access_token
            headers['Authorization'] = f'Bearer {new_access_token}'
            response = requests.get(f'{RECIPE_SERVICE_URL}/specialrecipes/', headers=headers)
            if response.status_code == 200:
                recipes = response.json()
                return render(request, 'create_recipe.html', {'recipes': recipes})
        messages.error(request, 'Session expired. Please log in again.')
        return redirect(next_url)
    else:
        messages.error(request, 'Failed to retrieve recipes.')
        return redirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        next_url = request.GET.get('next', '/')

        auth_url = f'{USER_SERVICE_URL}/token/'
        data = {'username': username, 'password': password}

        try:
            response = requests.post(auth_url, data=data)
            if response.status_code == 200:
                tokens = response.json()
                access_token = tokens['access']
                refresh_token = tokens['refresh']

                request.session['access_token'] = access_token
                request.session['refresh_token'] = refresh_token
                request.session['username'] = username

                messages.success(request, f'Logged in as {username}')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password')
                return redirect(next_url)
        except Exception as e:
            messages.error(request, 'An error occurred during login.')
            return redirect(next_url)
    else:
        return redirect('/')
    
#Hjälpfunktion vilket kallas på i det fallet vi får ett 401 error vid authentication mot en annan microservice. 
def refresh_token_on_401(refresh_token): 
    refresh_url = f'{USER_SERVICE_URL}/token/refresh/'
    data = {'refresh': refresh_token}
    response = requests.post(refresh_url, data=data)
    if response.status_code == 200:
        tokens = response.json()
        return tokens['access']
    else:
        return None

    
def logout_view(request):
    request.session.flush()
    next_url = request.GET.get('next', '/')
    messages.success(request, 'Logged out successfully')
    return redirect(next_url)
