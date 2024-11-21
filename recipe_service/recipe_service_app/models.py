from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)  

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=500)
    time = models.IntegerField()
    cost = models.IntegerField()
    kcal = models.IntegerField()
    portions = models.IntegerField()
    imageurl = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Disregard users for now

    def __str__(self):
        return self.title

class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='instructions')
    step_number = models.IntegerField()
    instruction = models.CharField(max_length=250)

    def __str__(self):
        return f"Step {self.step_number} for {self.recipe.title}"
    
class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)
    amount = models.IntegerField()
