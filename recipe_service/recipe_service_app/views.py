
# recipe_service/views.py

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Recipe
from .serializers import RecipeSerializer, RecipeDetailsSerializer

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
                pass  # If limit is not an integer, ignore it
        return queryset
    
class RecipeDetailsView(generics.RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailsSerializer  # Use RecipeSerializer if separate details serializer isn't needed
    lookup_field = 'id'  # Default is 'pk'; adjust if needed