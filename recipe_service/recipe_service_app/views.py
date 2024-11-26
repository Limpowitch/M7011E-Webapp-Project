
# recipe_service/views.py

from rest_framework import generics
from .models import Recipe, Category
from .serializers import RecipeSerializer, RecipeDetailsSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

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

#Följande klass är enbart som exempel för att visa hur vi använder oss av JWT authentication
class SpecialRecipeListView(generics.ListAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated] #om inte authenticated, returnera 401 error

    #begå queries etc...
    
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