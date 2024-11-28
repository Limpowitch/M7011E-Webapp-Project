from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import RecipeListView, RecipeDetailsView, CategoryRecipesView, CategoryListView, UnitListView, RecipeCreateView, UserRecipesAPIView

urlpatterns = [
    path('recipes/', RecipeListView.as_view(), name='recipe-list'),
    path('recipes/<int:id>/', RecipeDetailsView.as_view(), name='recipe-detail'),
    path('category/<str:category>/', CategoryRecipesView.as_view(), name='category-recipes'),
    path('categories/', CategoryListView.as_view(), name='category-llist'),
    path('units/', UnitListView.as_view(), name='unit-list'),
    path('create_recipe/', RecipeCreateView.as_view(), name='create-recipe'),
    path('<str:username>/recipes/', UserRecipesAPIView.as_view(), name='user-recipes'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)