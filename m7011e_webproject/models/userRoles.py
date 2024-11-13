#Users for the prject
from django.db import models

class admin(models.Model): 
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    permission = models.CharField(max_length=10)
    
    
class user(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phoneNumber = models.CharField(max_length=50)
    twoFactorAuth = models.BooleanField(False)
    permission = models.CharField(max_length=10)
    
class superUser(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phoneNumber = models.CharField(max_length=50)
    twoFactorAuth = models.BooleanField(False)
    permission = models.CharField(max_length=10)
 
