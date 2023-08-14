from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED
)


class AddAndDeleteViewMixin:
    add_serializer = None

    def add_and_delete(self, obj_id, manager):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)

        managers = {
            'follow': user.follow,
            'favorite': user.favorite_recipes,
            'shopping_cart': user.shopping_cart_recipes,
        }
        manager = managers[manager]

        obj = get_object_or_404(self.queryset, id=obj_id)
        serializer = self.add_serializer(
            obj, context={'request': self.request}
        )
        obj_exist = manager.filter(id=obj_id).exists()

        if (self.request.method in ('GET', 'POST',)) and not obj_exist:
            manager.add(obj)
            return Response(serializer.data, status=HTTP_201_CREATED)

        if (self.request.method in ('DELETE',)) and obj_exist:
            manager.remove(obj)
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_400_BAD_REQUEST)