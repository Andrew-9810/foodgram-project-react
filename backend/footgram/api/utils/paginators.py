from rest_framework.pagination import PageNumberPagination


class PageLimitPaginator(PageNumberPagination):
    """Пагинация по страницам."""
    page_size = 5
    page_size_query_param = 'limit'
