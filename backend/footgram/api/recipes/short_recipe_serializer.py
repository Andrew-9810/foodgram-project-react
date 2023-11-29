from recipes.models import Recipe
from rest_framework import serializers


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Рецепты автора, сокращеннный вариант."""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
