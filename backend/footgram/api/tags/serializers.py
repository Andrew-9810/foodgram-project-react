from rest_framework import serializers

from recipes.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор Тегов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
