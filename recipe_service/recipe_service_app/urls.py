from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import RecipeListView

urlpatterns = [
    path('recipes/', RecipeListView.as_view(), name='recipe-list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)