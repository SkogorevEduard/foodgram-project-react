from rest_framework import viewsets

from .models import Tag
from .serializers import TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с тэгом."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
