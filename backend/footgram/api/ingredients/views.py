from rest_framework import viewsets

from recipes.models import Ingredient
from .filters import IngredientSearchFilter
from .serializers import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет Ингридиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
