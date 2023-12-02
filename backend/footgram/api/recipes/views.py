from django.db.models import Sum
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.recipes.filters import RecipeFilter
from api.recipes.permissions import OwnerOrReadOnly, ReadOnly
from api.recipes.serializers import (
    CreateAndUpdateRecipeSerializer,
    RecipeSerializer,
    FavoriteRecipeSerializer
)
from api.recipes.short_recipe_serializer import ShortRecipeSerializer
from api.utils.paginators import PageLimitPaginator
from recipes.models import (
    AmountIngredient, FavoriteRecipe, Ingredient, Recipe, ShoppingList
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

    @action(detail=True, methods=['POST'])
    def favorite(self, request, pk):
        """Добавление рецепта в избранное."""
        try:
            recipe = get_object_or_404(Recipe, pk=pk)
        except Http404:
            raise exceptions.ValidationError(
                'Указан несуществующий рецепт.'
            )
        serializer = FavoriteRecipeSerializer(
            data={'recipe': pk},
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            out_serializer = ShortRecipeSerializer(
                recipe,
                context={'request': request}
            )
            return Response(
                out_serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
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
        FavoriteRecipe.objects.filter(
            user=user,
            recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'])
    def shopping_cart(self, request, pk=None):
        """Добавление рецепта в список покупок."""
        user = self.request.user
        if not Recipe.objects.filter(pk=pk).exists():
            raise exceptions.ValidationError(
                'Попытка добавить несуществующий рецепт в избранное.'
            )
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

    def get_permissions(self):
        """Выбор ограничения."""
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()
