from rest_framework import serializers
from recipes.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор Ингридиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
