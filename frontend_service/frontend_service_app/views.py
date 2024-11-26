from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
import requests

RECIPE_SERVICE_URL = 'http://localhost:8001'
USER_SERVICE_URL = 'http://localhost:8002'

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

def recipe_detail(request, id):
    response = requests.get(f'{RECIPE_SERVICE_URL}/recipes/{id}/')
    recipe = response.json()
    return render(request, 'recipe.html', {'recipe': recipe})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        next_url = request.GET.get('next', '/')

        auth_url = f'{USER_SERVICE_URL}/authenticate/'
        data = {'username': username, 'password': password}

        try:
            response = requests.post(auth_url, data=data)
            if response.status_code == 200:
                user_data = response.json()
                user_id = int(user_data['id'])
                username = str(user_data['username'])

                request.session['user_id'] = user_id
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
    
def logout_view(request):
    request.session.flush()
    next_url = request.GET.get('next', '/')
    messages.success(request, 'Logged out successfully')
    return redirect(next_url)
