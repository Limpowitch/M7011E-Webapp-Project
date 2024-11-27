import os
import uuid
from django.conf import settings
from rest_framework import serializers
from django.db.models import Avg
from .models import Recipe, Category, Instruction, Ingredient, Unit, Rating, Comment
import json

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ['step_number', 'instruction']

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name']


class IngredientSerializer(serializers.ModelSerializer):
    unit = UnitSerializer(read_only=True)

    class Meta:
        model = Ingredient
        fields = ['ingredient', 'unit', 'amount']

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
            'average_rating', 
        ]

    def get_average_rating(self, obj):
        average = obj.ratings.aggregate(avg=Avg('rating'))['avg']
        return round(average, 2) if average is not None else 0

class RecipeCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    instructions = serializers.CharField()  
    ingredients = serializers.CharField() 
    image = serializers.ImageField(write_only=True, required=False)  

    class Meta:
        model = Recipe
        fields = [
            'title',
            'category',
            'description',
            'time',
            'cost',
            'kcal',
            'portions',
            'instructions',
            'ingredients',
            'imageurl',  
            'image',
        ]
        read_only_fields = ['imageurl']

    def create(self, validated_data):
        instructions_data = validated_data.pop('instructions')
        ingredients_data = validated_data.pop('ingredients')
        image = validated_data.pop('image', None)

        instructions = json.loads(instructions_data)
        ingredients = json.loads(ingredients_data)

        if image:
            print(f"Image received: {image.name}, Content-Type: {image.content_type}")
            ext = os.path.splitext(image.name)[1]  
            unique_filename = f"{uuid.uuid4()}{ext}"
            image_path = os.path.join(unique_filename)
            full_path = os.path.join(settings.MEDIA_ROOT, image_path)

            with open(full_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            image_url = self.context['request'].build_absolute_uri(settings.MEDIA_URL + image_path)
        else:
            print("No image received.")
            image_url = 'http://localhost:8001/media/Kanelbullar.jpg'

        recipe = Recipe.objects.create(**validated_data, imageurl=image_url)

        for instruction_data in instructions:
            Instruction.objects.create(recipe=recipe, **instruction_data)

        for ingredient_data in ingredients:
            unit_id = ingredient_data['unit']
            try:
                unit = Unit.objects.get(id=unit_id)
                print("found unit: ", unit)
            except Unit.DoesNotExist:
                raise serializers.ValidationError(f"Unit with id {unit_id} does not exist.")
            Ingredient.objects.create(
                recipe=recipe,
                ingredient=ingredient_data['ingredient'],
                unit=unit,
                amount=ingredient_data['amount']
            )

        return recipe