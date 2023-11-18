from rest_framework import viewsets
from recipes.models import Tag
from .serializers import TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет Тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
