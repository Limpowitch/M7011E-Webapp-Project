
# recipe_service/views.py

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Recipe, Category
from .serializers import RecipeSerializer, RecipeDetailsSerializer
from django.shortcuts import get_object_or_404

class RecipeListView(generics.ListAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        queryset = Recipe.objects.all()
        limit = self.request.query_params.get('limit', None)
        if limit is not None:
            try:
                limit = int(limit)
                queryset = queryset.order_by('?')[:limit]
            except ValueError:
                pass  
        return queryset
    
class CategoryRecipesView(generics.ListAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        category_name = self.kwargs.get('category')
        category = get_object_or_404(Category, name=category_name)
        return Recipe.objects.filter(category=category)

    
class RecipeDetailsView(generics.RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailsSerializer  
    lookup_field = 'id'  