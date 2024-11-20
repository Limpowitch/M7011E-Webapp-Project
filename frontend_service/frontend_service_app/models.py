from django.db import models

# Create your models here.

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    instructions = models.TextField()
    ingredients = models.TextField()
    time = models.IntegerField()
    cost = models.IntegerField()
    kcal = models.IntegerField()
    portions = models.IntegerField()
    imageurl = models.TextField()
    user = models.IntegerField()
