from rest_framework import serializers
from .models import Recipe, Category, Instruction, Ingredient

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ['id', 'step_number', 'instruction']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'ingredient', 'amount']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'category',
            'description',
            'time',
            'cost',
            'kcal',
            'portions',
            'imageurl',
        ]

class RecipeDetailsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    instructions = InstructionSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    
    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'category',
            'description',
            'time',
            'cost',
            'kcal',
            'portions',
            'imageurl',
            'instructions',
            'ingredients',
        ]

