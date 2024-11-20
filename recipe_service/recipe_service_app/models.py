from django.db import models

# Create your models here.

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    category = models.IntegerField()
    description = models.CharField(max_length=500)
    instructions = models.IntegerField()
    ingredients = models.IntegerField()
    time = models.IntegerField()
    cost = models.IntegerField()
    kcal = models.IntegerField()
    portions = models.IntegerField()
    imageurl = models.CharField(max_length=1000)
    user = models.IntegerField()

    def __str__(self):
        return self.title
