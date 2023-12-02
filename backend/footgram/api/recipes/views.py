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
    FavoriteRecipeSerializer,
    RecipeSerializer,
    ShoppingListSerializer
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

    def creat_fav_shop_cart(self, request, pk, serializer):
        """Добавление рецепта в избранное, корзину."""
        try:
            recipe = get_object_or_404(Recipe, pk=pk)
        except Http404:
            raise exceptions.ValidationError(
                'Указан несуществующий рецепт.'
            )
        serializer = serializer
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

    def del_fav_shop_cart(self, request, pk, model):
        """Удалаение рецепта из избраного и корзины."""
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if not model.objects.filter(
                user=user,
                recipe=recipe
        ).exists():
            raise exceptions.ValidationError(
                'Рецепт удален!'
            )
        model.objects.filter(
            user=user,
            recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'])
    def favorite(self, request, pk):
        """Добавление рецепта в избранное."""
        serializer = FavoriteRecipeSerializer(
            data={'recipe': pk},
            context={'request': request}
        )
        return self.creat_fav_shop_cart(
            request=request,
            pk=pk,
            serializer=serializer
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        """Удаление рецепта из избранного."""
        model = FavoriteRecipe
        return self.del_fav_shop_cart(pk=pk, request=request, model=model)

    @action(detail=True, methods=['POST'])
    def shopping_cart(self, request, pk):
        """Добавление рецепта в список покупок."""

        serializer = ShoppingListSerializer(
            data={'recipe': pk},
            context={'request': request}
        )
        return self.creat_fav_shop_cart(
            request=request,
            pk=pk,
            serializer=serializer
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        """Удаление рецепта из списка покупок."""
        model = ShoppingList
        return self.del_fav_shop_cart(pk=pk, request=request, model=model)

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
            )
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
