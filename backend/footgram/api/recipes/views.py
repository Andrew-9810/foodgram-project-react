from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import (
    AmountIngredient, FavoriteRecipe, Recipe, ShoppingList, Ingredient
)
from api.users.serializers import ShortRecipeSerializer
from api.utils.paginators import PageLimitPaginator
from .filters import RecipeFilter
from .serializers import CreateAndUpdateRecipeSerializer, RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет Рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageLimitPaginator
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        """Определение метода работы с экземпляром."""
        if self.action == 'create' or self.action == 'partial_update':
            return CreateAndUpdateRecipeSerializer
        return RecipeSerializer

    @action(detail=True, methods=['POST'])
    # Разрешена работа с одним объектом(не с коллекцией) по методу пост
    def favorite(self, request, pk=None):
        """Определение рецепта в избранном."""
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if FavoriteRecipe.objects.filter(
                user=user,
                recipe=recipe
        ).exists():
            raise exceptions.ValidationError('Рецепт добавлен в избранное.')
        FavoriteRecipe.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(
            recipe,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        """Удаление рецепта из избранного."""
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if not FavoriteRecipe.objects.filter(
                user=user,
                recipe=recipe
        ).exists():
            raise exceptions.ValidationError(
                'Рецепт удален из избраного!'
            )
        favorite = get_object_or_404(FavoriteRecipe,
                                     user=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'])
    def shopping_cart(self, request, pk=None):
        """Добавление рецепта в список покупок."""
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if ShoppingList.objects.filter(
                user=user,
                recipe=recipe
        ).exists():
            raise exceptions.ValidationError(
                'Рецепт в списке покупок!'
            )
        ShoppingList.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(
            recipe,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        """Удаление рецепта из списка покупок."""
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if not ShoppingList.objects.filter(
                user=user,
                recipe=recipe
        ).exists():
            raise exceptions.ValidationError(
                'Рецепта удален из списка покупок!'
            )
        shopping_cart = get_object_or_404(
            ShoppingList,
            user=user,
            recipe=recipe
        )
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        """Загрузить список покупок."""
        shopping_cart = ShoppingList.objects.filter(user=self.request.user)
        recipes = []
        for item in shopping_cart:
            recipes.append(item.recipe.id)
        shopping_list = AmountIngredient.objects.filter(
            recipe__in=recipes
        ).values(
            'ingredient'
        ).annotate(
            amount=Sum('amount')
        )
        shopping_list_text = 'Список покупок: \n'
        for item in shopping_list:
            ingredient = Ingredient.objects.get(pk=item['ingredient'])
            amount = item['amount']
            shopping_list_text += (
                f'{ingredient.name}, {amount} '
                f'{ingredient.measurement_unit}\n'
            )
        response = HttpResponse(shopping_list_text, content_type="text/plain")
        response['Content-Disposition'] = (
            'attachment; filename=shopping-list.txt'
        )
        return response
