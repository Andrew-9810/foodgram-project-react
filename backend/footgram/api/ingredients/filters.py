from rest_framework.filters import SearchFilter


class IngredientSearchFilter(SearchFilter):
    """Фильтр по Ингридиентам."""
    search_param = 'name'
