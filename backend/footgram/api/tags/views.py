from api.tags.serializers import TagSerializer
from rest_framework import viewsets
from recipes import models


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет Тегов."""
    queryset = models.Tag.objects.all()
    serializer_class = TagSerializer
