from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse

from .filters import RecipeFilter
from .models import Recipes
from .permissions import AuthorStaffOrReadOnly
from .serializers import (RecipesCreateOrUpdateSerializer, RecipeSerializer,
                          FollowRecipesShortSerializer)
from .mixins import AddAndDeleteViewMixin
from users.pagination import LimitPageNumberPagination
from .services import get_shopping_list


class RecipeViewSet(ModelViewSet, AddAndDeleteViewMixin):
    """Вьюсет для работы с рецептами."""
    queryset = Recipes.objects.select_related('author')
    permission_classes = (AuthorStaffOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = LimitPageNumberPagination
    add_serializer = FollowRecipesShortSerializer

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipesCreateOrUpdateSerializer
        return RecipeSerializer

    @action(
        methods=['get', 'post', 'delete'],
        detail=True
    )
    def favorite(self, request, pk):
        return self.add_and_delete(pk, 'favorite')

    @action(
        methods=['get', 'post', 'delete'],
        detail=True
    )
    def shopping_cart(self, request, pk):
        return self.add_and_delete(pk, 'shopping_cart')

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        user = request.user
        buy_list_text = get_shopping_list(user)
        response = FileResponse(buy_list_text, content_type="text/plain")
        response['Content-Disposition'] = (
            'attachment; filename=shopping-list.txt'
        )
        return response
    