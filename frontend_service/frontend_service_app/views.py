import os
import uuid
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import json
import theStringManager
from django.shortcuts import render, redirect

from .forms import RegistrationForm
from .forms import PasswordChangeForm
from django.contrib.auth.models import User

from django.utils import timezone
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from decouple import config
from django.contrib.auth import authenticate, login

RECIPE_SERVICE_URL = 'http://localhost:8001'
USER_SERVICE_URL = 'http://localhost:8002'

def homepage(request):
    limit = 4
    
    response = requests.get(f'{RECIPE_SERVICE_URL}/recipes/', params={'limit': limit})
    recipes = response.json()
    return render(request, 'homepage.html', {'recipes': recipes})

def category(request, category):
    access_token = request.session.get('access_token')
    headers = {}

    if access_token:
        headers['Authorization'] = f'Bearer {access_token}'

    response = requests.get(f'{RECIPE_SERVICE_URL}/category/{category}/', headers=headers)

    if response.status_code == 200:
        recipes = response.json()
    else:
        recipes = []
        print(f"Error fetching recipes: {response.status_code}, {response.text}")

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
        
def delete_recipe(request, id):

    access_token = request.session.get('access_token')

    if not access_token:
        messages.error(request, 'Log in to delete recipes')
        return redirect('login')

    headers = {
        'Authorization': f"Bearer {request.session.get('access_token')}",
    }
    try:
        response = requests.delete(f"{RECIPE_SERVICE_URL}/delete_recipe/{id}/", headers=headers)
        if response.status_code == 204:
            print(request, "Recipe deleted successfully!")
        else:
            print(request, "Failed to delete the recipe.")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        messages.error(request, "An error occurred. Please try again.")
    return redirect('user_information')

def generate_2fa():
    return str(random.randint(100000, 999999))
               

def send_2fa_smtp(to_email, code):
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = config('EMAIL_HOST_USER', default='noreply@localhost')
    smtp_password = config('EMAIL_HOST_PASSWORD', default='password')
    from_email = smtp_username
    subject = "Here is your 2FA code"

    body = f"Your 2FA code is: {code} \n\nThis code will expire in 5 minutes."
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    
    try: 
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.local_hostname="localhost"
            server.set_debuglevel(1)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())
        print(f"2FA code sent to {to_email}")
    except Exception as e:
        print(f"Failed to send 2FA code to {to_email}: {e}")


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            user = User.objects.get(username=username)
            user_email = user.email  
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('homepage')
        


        auth_url = f'{USER_SERVICE_URL}/token/'
        data = {'username': username, 'password': password}
        response = requests.post(auth_url, data=data)

        if response.status_code == 200:
            code = generate_2fa()
            print(code)
            expires_at = timezone.now() + timedelta(minutes=5)
            request.session['user_code_2fa'] = code
            request.session['user_code_expires_2fa'] = expires_at.isoformat()

            if not user_email:
                messages.error(request, 'No email found for user.')
                print("ingen mail")
            send_2fa_smtp(user_email, code)

            request.session['pending_username'] = username
            request.session['pending_password'] = password

            messages.success(request, '2FA code sent to your email.')
            return redirect('verify_2fa')  
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('homepage')  
            
def two_way_auth_view(request):
    if request.method == 'POST':
        user_input_code = request.POST.get('user_code_2fa', '')
        session_code = request.session.get('user_code_2fa')
        session_code_expires = request.session.get('user_code_expires_2fa')
        username = request.session.get('pending_username')
        password = request.session.get('pending_password')
        next_url = request.session.get('next_url')
        
        if not session_code or not session_code_expires:
            messages.error(request, 'No 2FA session data found or expired.')
            return redirect('homepage') 

        try:
            session_code_expires = datetime.fromisoformat(session_code_expires)
        except ValueError:
            messages.error(request, 'Invalid session expiration.')
            return redirect('homepage')

        if timezone.now() > session_code_expires:
            messages.error(request, 'Code has expired, please try again.')
            return redirect('homepage')

        if user_input_code == session_code:
            # External auth call to retrieve tokens
            auth_url = f'{USER_SERVICE_URL}/token/'
            data = {'username': username, 'password': password}
            response = requests.post(auth_url, data=data)
            
            if response.status_code == 200:
                tokens = response.json()
                access_token = tokens['access']
                refresh_token = tokens['refresh']

                # Store tokens in session as needed
                request.session['access_token'] = access_token
                request.session['refresh_token'] = refresh_token
                request.session['username'] = username

                # Authenticate and log the user into Django's session
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                else:
                    messages.error(request, 'Django authentication failed.')
                    return redirect('login')

                # Clean up 2FA and temporary session data
                request.session.pop('user_code_2fa', None)
                request.session.pop('user_code_expires_2fa', None)
                request.session.pop('pending_username', None)
                request.session.pop('pending_password', None)
                request.session.pop('next_url', None)

                messages.success(request, f'Logged in as {username} with 2FA.')
                return redirect(next_url or 'homepage')
            else:
                messages.error(request, 'Failed to log in. Please try again.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid 2FA code. Please try again.')
            return redirect('verify_2fa')
    return render(request, 'verify_2fa.html')

def logout_view(request):
    request.session.flush()
    messages.success(request, 'Logged out successfully')
    return redirect('homepage')
    
def refresh_token_on_401(refresh_token): 
    refresh_url = f'{USER_SERVICE_URL}/token/refresh/'
    data = {'refresh': refresh_token}
    response = requests.post(refresh_url, data=data)
    if response.status_code == 200:
        tokens = response.json()
        return tokens['access']
    else:
        return None

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            payload = {
                'username': data['username'],
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'password1': data['password1'],
                'password2': data['password2'],
            }
            try:
                response = requests.post(f"{USER_SERVICE_URL}/register/", json=payload)
                if response.status_code == 201:
                    messages.success(request, "Registration successful! Please log in.")
                    return redirect('homepage')  
                else:
                    errors = response.json().get('errors', {})
                    for field, error in errors.items():
                        messages.error(request, f"{field}: {error}")
            except Exception as e:
                print(f"Error during API call: {e}")
                messages.error(request, "An error occurred. Please try again.")
        else:
            for field, error in form.errors.items():
                messages.error(request, f"{field}: {error}")
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def change_password(request):
    access_token = request.session.get('access_token')
    
    if not access_token:
        messages.error(request, 'Please log in to change your password')
        return redirect('login')

    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            payload = {
                'current_password': data['current_password'],
                'new_password1': data['new_password1'],
                'new_password2': data['new_password2'],
            }
            headers = {
                'Authorization': f"Bearer {request.session.get('access_token')}",
            }
            try:
                response = requests.post(f"{USER_SERVICE_URL}/change-password/", json=payload, headers=headers)
                if response.status_code == 200:
                    messages.success(request, "Password updated successfully.\n" + theStringManager.success())
                    return redirect('homepage')
                else:
                    errors = response.json().get('errors', {})
                    for field, error in errors.items():
                        messages.error(request, f"{field}: {error}")
            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
                messages.error(request, "An error occurred. Please try again.")
    else:
        form = PasswordChangeForm()
    return render(request, 'change_password.html', {'form': form})

def delete_account(request):

    access_token = request.session.get('access_token')

    if not access_token:
        messages.error(request, 'Please log in to delete your account')
        return redirect('user_information')

    if request.method == 'POST':
        headers = {
            'Authorization': f"Bearer {request.session.get('access_token')}",
        }
        try:
            response = requests.delete(f"{USER_SERVICE_URL}/delete-account/", headers=headers)
            if response.status_code == 204:
                request.session.flush()
                messages.success(request, "Your account has been deleted. We're sad to see you go! But before you go, "
                                          "have some wise words: " + theStringManager.wise_words())
                return redirect('homepage')
            else:
                messages.error(request, response.json().get('error', 'Failed to delete account.'))
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            messages.error(request, "An error occurred. Please try again.")
    return redirect('user_information')

def user_information(request):
    access_token = request.session.get('access_token')

    if not access_token:
        messages.error(request, 'Please log in to delete your account')
        return redirect('login')
    
    username = request.session.get('username')
    
    response = requests.get(f'{RECIPE_SERVICE_URL}/{username}/recipes/')
    recipes = response.json()
    return render(request, 'user_information.html', {'recipes': recipes})

def edit_recipe(request, id):
    access_token = request.session.get('access_token')
    refresh_token = request.session.get('refresh_token')

    if not access_token:
        messages.error(request, 'Please log in to edit a recipe.')
        return redirect('login')

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    if request.method == 'GET':
        try:
            categories_response = requests.get(f'{RECIPE_SERVICE_URL}/categories/', headers=headers)
            units_response = requests.get(f'{RECIPE_SERVICE_URL}/units/', headers=headers)
            recipe_response = requests.get(f'{RECIPE_SERVICE_URL}/recipes/{id}/', headers=headers)

            if recipe_response.status_code == 200:
                recipe = recipe_response.json()
                print('successfully retrieved recipe data')
            else:
                print(request, 'Recipe not found.')
                return redirect('user_information')
            
            if 'instructions' in recipe:
                recipe_instructions = [step['instruction'] for step in recipe['instructions'] if 'instruction' in step]
                recipe['instructions'] = recipe_instructions

            if categories_response.status_code == 200 and units_response.status_code == 200:
                categories = categories_response.json()
                units = units_response.json()
                print('här!!!')

                return render(request, 'edit_recipe.html', {
                    'categories': categories,
                    'units': units,
                    'recipe': recipe,  
                })
            
            elif (categories_response.status_code == 401 or units_response.status_code == 401):
                print('eller här!!')
                new_access_token = refresh_token_on_401(refresh_token)
                if new_access_token:
                    request.session['access_token'] = new_access_token
                    headers['Authorization'] = f'Bearer {new_access_token}'
                    categories_response = requests.get(f'{RECIPE_SERVICE_URL}/categories/', headers=headers)
                    units_response = requests.get(f'{RECIPE_SERVICE_URL}/units/', headers=headers)
                    recipe_response = requests.get(f'{RECIPE_SERVICE_URL}/recipes/{id}/', headers=headers)

                    if recipe_response.status_code == 200:
                        recipe = recipe_response.json()
                    else:
                        print(request, 'Recipe not found.')
                        return redirect('user_information')

                    if categories_response.status_code == 200 and units_response.status_code == 200:
                        categories = categories_response.json()
                        units = units_response.json()

                        return render(request, 'edit_recipe.html', {
                            'categories': categories,
                            'units': units,
                            'recipe': recipe,  
                        })
            
            else:
                print(request, 'Failed to load necessary data.')
                return redirect('user_information')

        except Exception as e:
            print(request, 'An error occurred while fetching data.')
            return redirect('user_information')
        
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

        response = requests.put(
            f'{RECIPE_SERVICE_URL}/edit_recipe/{id}/',
            data=data,
            files=files,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        if response.status_code == 200:
            messages.success(request, 'Recipe updated successfully!\n' + theStringManager.meow())
            return redirect('user_information')
        else:
            messages.error(request, 'Error while updating the recipe.')
            return redirect('edit_recipe', id=id)


def admin_view(request):
    access_token = request.session.get('access_token')

    if not access_token:
        messages.error(request, 'Please log in to delete your account')
        return redirect('homepage')
        
    limit = None
    
    response = requests.get(f'{RECIPE_SERVICE_URL}/recipes/', params={'limit': limit})
    recipes = response.json()
    print(recipes)
    return render(request, 'admin_page.html', {'recipes': recipes}) 

def approve_recipe(request, id):
    access_token = request.session.get('access_token')

    if not access_token:
        messages.error(request, 'Please log in.')
        return redirect('homepage')

    approve_url = f"{RECIPE_SERVICE_URL}/approve_recipe/{id}/"
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.put(approve_url, headers=headers)
    if response.status_code == 200:
        messages.success(request, 'Recipe approved!')
    else:
        messages.error(request, 'Failed to approve recipe.')

    return redirect('admin_page') 

def administrate_users(request):
    access_token = request.session.get('access_token')

    if not access_token:
        messages.error(request, 'Please log in.')
        return redirect('homepage')
    
    headers={'Authorization': f'Bearer {access_token}'}
    
    users_url = f"{USER_SERVICE_URL}/retrieve_users/"
    response = requests.get(users_url, headers=headers)
    users = response.json() if response.status_code == 200 else []
    return render(request, 'administrate_users.html', {'users': users})

def change_to_superuser(request, id):
    access_token = request.session.get('access_token')

    if not access_token:
        messages.error(request, 'You must be logged in to perform this action.')
        return redirect('login')  # Adjust this redirect as needed

    user_service_url = f"{USER_SERVICE_URL}/change_to_superuser/{id}/"

    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(user_service_url, headers=headers)

    if response.status_code == 200:
        messages.success(request, f'User {id} has been set as superuser.')
    else:
        messages.error(request, f'Failed to change user {id} to superuser.')

    return redirect('administrate_users')


