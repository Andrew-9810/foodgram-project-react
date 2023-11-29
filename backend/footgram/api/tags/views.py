from api.tags.serializers import TagSerializer
from rest_framework import viewsets
from recipes.models import Tag


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет Тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
