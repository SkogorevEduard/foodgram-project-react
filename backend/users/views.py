from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, exceptions
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .models import Follow, User
from .serializers import (FollowSerializer)
from .pagination import LimitPageNumberPagination


class CustomUserViewSet(UserViewSet):
    """Вьюсет для кастомной модели пользователя."""
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitPageNumberPagination

    @action(
        detail=True,
        methods=('post', 'delete')
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            if user == author:
                raise exceptions.ValidationError(
                    'Подписка на самого себя запрещена.'
                )
            if Follow.objects.filter(
                user=user,
                author=author
            ).exists():
                raise exceptions.ValidationError('Подписка уже существует.')
            Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(author,
                                          context={'request': request})
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        if self.request.method == 'DELETE':
            if not Follow.objects.filter(
                user=user,
                author=author
            ).exists():
                raise exceptions.ValidationError(
                    'Подписка не была оформлена, либо уже удалена.'
                )
            get_object_or_404(Follow, user=user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated, )
    )
    def subscriptions(self, request):
        return self.get_paginated_response(
            FollowSerializer(
                self.paginate_queryset(
                    User.objects.filter(following__user=request.user)
                ),
                many=True,
                context={'request': request},
            ).data
        )
