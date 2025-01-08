# M7011E Webapp Project

A simple recipe website written in python utilizing the Django backend framework, and HTML, Tailwind-CSS, and Typescript for the frontend. 

The website utilize a microservice architecture and is thus divided into three different services:

- Frontend_service
    - Handles all logic coupled to the displaying of the frontend
- Recipe_service
    - Handles all logic connected to retrieval and posting of recipe data from and to the connected database
- User_service
    - Handles handling of users alongside creation and distibution of JWT tokens
- (There's an additional fourth service Search_service, but it's not used)

As of now the website only works for Windows because of how filepaths are handled by NPM.

In order to get the website to run, the following commands needs to be run in a a terminal for each service:

- Frontend_service
    - pip install -r requirements.txt
    - python manage.py runserver 8000

- Recipe_service
    - pip install -r requirements.txt
    - python manage.py runserver 8001

- User_service
    - pip install -r requirements.txt
    - python manage.py runserver 8002

Once all the requirements are met, you can then access the website by going to localhost:8000

# Features

The website currently have a few simple features, with more features unlocked if you're a registered user:

- Unregistered
    - Read recipes posted by other users
    - Register a new authenticated user

- Registered
    - Create, edit, and delete recipes uploaded by you
    - Change password
    - Delete your user account

- Registered Super User
    - Directly upload a recipe without admin approval

When a recipe is uploaded it gets placed in a pending queue to be accepted by a website admin in order to help with content moderation.
An Exception to this is made for registered super users which is a role given out by website administrators.

The website has a system to handle comments and ratings on a recipe, but for now doesn't have a mechanic to add such comments/ratings to a recipe, further work is needed here.

# Security and Authentication

The website utilize djangos pre-built security features, thus making sure that threats such as SQL-Injections are protected against. 

For additional security, at the point of login, a 2FA code will be sent out to the users connected email which the website will ask the user to insert before the user is allowed in.

For authentication between the services, the website utilize simple_JWT, thus making sure that all API calls between the services are authorised and legitimate. 
