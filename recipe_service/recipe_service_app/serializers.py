from rest_framework import serializers
from django.db.models import Avg
from .models import Recipe, Category, Instruction, Ingredient, Unit, Rating, Comment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ['id', 'step_number', 'instruction']

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name']


class IngredientSerializer(serializers.ModelSerializer):
    unit = UnitSerializer(read_only=True)

    class Meta:
        model = Ingredient
        fields = ['id', 'ingredient', 'unit', 'amount']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment', 'created_at', 'user_id', 'recipe_id']

class RatingSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Rating
        fields = ['id', 'rating', 'user_id', 'recipe_id']


class RecipeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
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
    comments = CommentSerializer(many=True, read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

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
            'comments',
            'ratings',
            'average_rating',  # New field
        ]

    def get_average_rating(self, obj):
        average = obj.ratings.aggregate(avg=Avg('rating'))['avg']
        return round(average, 2) if average is not None else 0

