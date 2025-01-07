from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


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
    #image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    imageurl = models.CharField(max_length=1000, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='instructions')
    step_number = models.IntegerField()
    instruction = models.CharField(max_length=250)

    def __str__(self):
        return f"Step {self.step_number} for {self.recipe.title}"
    
class Unit(models.Model):
    name = models.CharField(max_length=10)  

    def __str__(self):
        return self.name
    
class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.CharField(max_length=100)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='ingredients')
    amount = models.IntegerField()

class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )

    class Meta:
        unique_together = ('recipe', 'user')

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)