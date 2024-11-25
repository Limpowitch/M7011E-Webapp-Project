from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import RecipeListView, RecipeDetailsView, CategoryRecipesView

urlpatterns = [
    path('recipes/', RecipeListView.as_view(), name='recipe-list'),
    path('recipes/<int:id>/', RecipeDetailsView.as_view(), name='recipe-detail'),
    path('category/<str:category>/', CategoryRecipesView.as_view(), name='category-recipes')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)