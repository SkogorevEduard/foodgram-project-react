from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

from .pagination import LimitPageNumberPagination
from .serializers import FollowSerializer
from recipes.mixins import AddAndDeleteViewMixin
from recipes.permissions import AuthorOrReadOnly


class CustomUserViewSet(UserViewSet, AddAndDeleteViewMixin):
    """Вьюсет для кастомной модели пользователя."""
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = LimitPageNumberPagination
    add_serializer = FollowSerializer

    @action(methods=['get', 'post', 'delete'],
            detail=True)
    def subscribe(self, request, id):
        return self.add_and_delete(id, 'follow')

    @action(
        detail=False,
        methods=('get',)
    )
    def subscriptions(self, request):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        authors = user.follow.all()
        pages = self.paginate_queryset(authors)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
