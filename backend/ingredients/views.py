from rest_framework import viewsets, filters

from .models import Ingredient
from .serializers import IngredientSerializer
from recipes.permissions import AdminOrReadOnly


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с ингредиентами."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']
