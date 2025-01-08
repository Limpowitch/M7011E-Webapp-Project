# recipe_service/views.py
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from django.http import Http404
from .models import Recipe, Category, Unit
from .serializers import CategorySerializer, RecipeCreateSerializer, RecipeSerializer, RecipeDetailsSerializer, RecipeUpdateSerializer, UnitSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView

class RecipeListView(generics.ListAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        queryset = Recipe.objects.filter(approved=True)
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
        user = self.request.user
        category_name = self.kwargs.get('category')
        category = get_object_or_404(Category, name=category_name)

        queryset = Recipe.objects.filter(category=category)
        if not user.is_superuser and not user.is_staff:
            queryset = queryset.filter(approved=True)

        print("Recipes returned:", queryset.values('id', 'title', 'approved'))
        return queryset
    
class RecipeDetailsView(generics.RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailsSerializer  
    lookup_field = 'id'  


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class UnitListView(generics.ListAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]

class RecipeCreateView(generics.CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def perform_create(self, serializer):
        user = self.request.user

        is_approved = user.is_superuser or user.is_staff

        serializer.save(user=user, approved=is_approved)

    def create(self, request, *args, **kwargs):
        print("Received data:", request.data)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            response_data = serializer.data

            response_data['approved'] = serializer.instance.approved
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            print("Validation Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRecipesAPIView(ListAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        username = self.kwargs['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404("User not found")

        recipes = Recipe.objects.filter(user=user)
        if not recipes.exists():
            raise Http404(f"No recipes found for user {username}")
        
        return recipes
    
class DeleteRecipeView(APIView):
    def delete(self, request, id):
        try:
            recipe = Recipe.objects.get(id=id)

            if recipe.user != request.user:
                return Response({'error': 'You are not authorized to delete this recipe.'}, status=status.HTTP_403_FORBIDDEN)

            recipe.delete()
            return Response({'message': 'Recipe deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Recipe.DoesNotExist:
            return Response({'error': 'Recipe not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class RecipeUpdateView(generics.UpdateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    lookup_field = 'id'         
    lookup_url_kwarg = 'id'     

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def update(self, request, *args, **kwargs):
        print("Received update data:", request.data)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.user != request.user:
            return Response(
                {'error': 'You are not authorized to update this recipe.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)