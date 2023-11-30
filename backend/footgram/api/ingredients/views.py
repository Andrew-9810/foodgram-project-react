from rest_framework import viewsets

from api.ingredients.filters import IngredientSearchFilter
from api.ingredients.serializers import IngredientSerializer
from recipes.models import Ingredient


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет Ингридиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
