from rest_framework import viewsets

from .models import Tag
from .serializers import TagSerializer
from recipes.permissions import AdminOrReadOnly


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с тэгом."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)
