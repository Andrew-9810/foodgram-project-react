from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.recipes.filters import RecipeFilter
from api.recipes.permissions import OwnerOrReadOnly, ReadOnly
from api.recipes.serializers import (
    CreateAndUpdateRecipeSerializer,
    FavoriteRecipeSerializer,
    RecipeSerializer,
    ShoppingListSerializer
)
from api.utils.paginators import PageLimitPaginator
from recipes.models import (
    AmountIngredient, FavoriteRecipe, Recipe, ShoppingList
)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет Рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageLimitPaginator
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        """Определение метода работы с экземпляром."""
        if self.action == 'create' or self.action == 'partial_update':
            return CreateAndUpdateRecipeSerializer
        return RecipeSerializer

    def create_favorite_shopping_cart(self, request, pk, class_serializer):
        """Добавление рецепта в избранное, корзину."""
        serializer = class_serializer(
            data={'recipe': pk},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_favorite_shopping_cart(self, request, pk, model, message):
        """Удалаение рецепта из избраного и корзины."""
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if not model.objects.filter(
                user=user,
                recipe=recipe
        ).exists():
            raise exceptions.ValidationError(message)
        model.objects.filter(
            user=user,
            recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'])
    def favorite(self, request, pk):
        """Добавление рецепта в избранное."""
        return self.create_favorite_shopping_cart(
            request=request,
            pk=pk,
            class_serializer=FavoriteRecipeSerializer
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        """Удаление рецепта из избранного."""
        return self.delete_favorite_shopping_cart(
            pk=pk, request=request, model=FavoriteRecipe,
            message='Pецепт не добавлен в избранное'
        )

    @action(detail=True, methods=['POST'])
    def shopping_cart(self, request, pk):
        """Добавление рецепта в список покупок."""
        return self.create_favorite_shopping_cart(
            request=request,
            pk=pk,
            class_serializer=ShoppingListSerializer
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        """Удаление рецепта из списка покупок."""
        return self.delete_favorite_shopping_cart(
            pk=pk, request=request, model=ShoppingList,
            message='Pецепт не добавлен в корзину'
        )

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        """Загрузить список покупок."""
        user = request.user
        shopping_list = AmountIngredient.objects.filter(
            recipe__in=ShoppingList.objects.filter(
                user=user
            ).values(
                'recipe'
            )).select_related('ingredient').all()

        shopping_list_text = 'Список покупок: \n'

        for item in shopping_list:
            shopping_list_text += (
                f'{item.ingredient.name}, {item.amount} '
                f'{item.ingredient.measurement_unit}\n'
            )

        response = HttpResponse(shopping_list_text, content_type="text/plain")
        response['Content-Disposition'] = (
            'attachment; filename=shopping-list.txt'
        )
        return response

    def get_permissions(self):
        """Выбор ограничения."""
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()
