from rest_framework import viewsets

from .models import Ingredient
from .serializers import IngredientSerializer
from recipes.filters import IngredientsSearchFilter


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с ингредиентами."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [IngredientsSearchFilter]
    search_fields = ['^name']
