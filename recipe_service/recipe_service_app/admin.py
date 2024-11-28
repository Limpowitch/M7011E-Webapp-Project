from django.contrib import admin
from .models import Recipe, Category, Instruction, Ingredient, Rating, Comment

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Category)
admin.site.register(Instruction)
admin.site.register(Ingredient)
admin.site.register(Rating)
admin.site.register(Comment)