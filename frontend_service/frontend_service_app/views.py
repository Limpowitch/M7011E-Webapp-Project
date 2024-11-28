import os
import uuid
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import json

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
    access_token = request.session.get('access_token')
    refresh_token = request.session.get('refresh_token')
    next_url = request.GET.get('next', '/')

    if not access_token:
        messages.error(request, 'Please log in to create a recipe.')
        return redirect('login')

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    if request.method == 'GET':
        try:
            categories_response = requests.get(f'{RECIPE_SERVICE_URL}/categories/', headers=headers)
            units_response = requests.get(f'{RECIPE_SERVICE_URL}/units/', headers=headers)

            if categories_response.status_code == 200 and units_response.status_code == 200:
                categories = categories_response.json()
                units = units_response.json()
                return render(request, 'create_recipe.html', {
                    'categories': categories,
                    'units': units,
                })
            elif categories_response.status_code == 401 or units_response.status_code == 401:  
                print("entering refresh token")     
                new_access_token = refresh_token_on_401(refresh_token)
                if new_access_token:
                    request.session['access_token'] = new_access_token
                    headers['Authorization'] = f'Bearer {new_access_token}'
                    categories_response = requests.get(f'{RECIPE_SERVICE_URL}/categories/', headers=headers)
                    units_response = requests.get(f'{RECIPE_SERVICE_URL}/units/', headers=headers)
                    if categories_response.status_code == 200 and units_response.status_code == 200:
                        categories = categories_response.json()
                        units = units_response.json()
                        print("successful 200")
                        return render(request, 'create_recipe.html', {
                            'categories': categories,
                            'units': units,
                        })
            else:
                print('Failed to load necessary data.')
                messages.error(request, 'Failed to load necessary data.')
                return redirect(next_url)
        except Exception as e:
            print("exception:", e)
            messages.error(request, 'An error occurred while fetching data.')
            return redirect('/')
    
    elif request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        time = request.POST.get('time')
        cost = request.POST.get('cost')
        kcal = request.POST.get('kcal')
        portions = request.POST.get('portions')
        instructions_list = request.POST.getlist('instructions[]')
        ingredient_names = request.POST.getlist('ingredients_name[]')
        ingredient_amounts = request.POST.getlist('ingredients_amount[]')
        ingredient_units = request.POST.getlist('ingredients_unit[]')

        
        instructions = [
            {"step_number": idx + 1, "instruction": instr}
            for idx, instr in enumerate(instructions_list)
        ]

        try:
            ingredients = [
                {"ingredient": name, "unit": int(unit_id), "amount": float(amount)}
                for name, unit_id, amount in zip(ingredient_names, ingredient_units, ingredient_amounts)
            ]
        except ValueError as ve:
            messages.error(request, f"Invalid ingredient data: {ve}")
            return redirect('create_recipe')
        
        image = request.FILES.get('image')

        files = {}
        if image:
            ext = os.path.splitext(image.name)[1]
            unique_filename = f"{uuid.uuid4()}{ext}"
            files['image'] = (unique_filename, image, image.content_type)

        data = {
            'title': title,
            'category': int(category_id),
            'description': description,
            'time': int(time) if time else None,
            'cost': float(cost) if cost else None,
            'kcal': int(kcal) if kcal else None,
            'portions': int(portions) if portions else None,
            'instructions': json.dumps(instructions),
            'ingredients': json.dumps(ingredients),
        }

        response = requests.post(f'{RECIPE_SERVICE_URL}/create_recipe/', headers=headers, data=data, files=files)

        if response.status_code == 201:
            print("big success")
            
            return redirect(next_url)
        else:
            error_message = response.json()
            print(error_message)
            return redirect('create_recipe')

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

def logout_view(request):
    request.session.flush()
    next_url = request.GET.get('next', '/')
    messages.success(request, 'Logged out successfully')
    return redirect(next_url)
    
def refresh_token_on_401(refresh_token): 
    refresh_url = f'{USER_SERVICE_URL}/token/refresh/'
    data = {'refresh': refresh_token}
    response = requests.post(refresh_url, data=data)
    if response.status_code == 200:
        tokens = response.json()
        return tokens['access']
    else:
        return None

    

