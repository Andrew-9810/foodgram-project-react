from rest_framework.filters import SearchFilter


# Прочитать про фильтр поиска, что можно изменить
class IngredientSearchFilter(SearchFilter):
    search_param = 'name'
