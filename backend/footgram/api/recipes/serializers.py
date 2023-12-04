from django.core import validators
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueTogetherValidator

from api.recipes.short_recipe_serializer import ShortRecipeSerializer
from api.tags.serializers import TagSerializer
from api.users.serializers import CustomUserSerializer
from recipes.models import (
    AmountIngredient,
    Ingredient,
    MAX_VALUE_VALIDATOR,
    MIN_VALUE_VALIDATOR,
    Recipe,
    Tag,
    FavoriteRecipe,
    ShoppingList
)


class AmountIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор количества ингредиентов в рецепте."""
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        validators=(
            validators.MinValueValidator(
                MIN_VALUE_VALIDATOR,
                message='Количество ингредиентов должно быть не менее 1.'
            ),
            validators.MaxValueValidator(
                MAX_VALUE_VALIDATOR,
                message='Превышен лимит количества ингредиентов.'
            )
        )
    )

    class Meta:
        model = AmountIngredient
        fields = ('id', 'amount')


class FullAmountIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор Суммы Ингридиетов."""
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = AmountIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор Рецептов."""
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        ingredients = AmountIngredient.objects.filter(recipe=obj)
        serializer = FullAmountIngredientSerializer(ingredients, many=True)
        return serializer.data

    def get_is_favorited(self, obj):
        return (
            self.context['request'].user.is_authenticated
            and obj.favorite.filter(
                user=self.context['request'].user
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        return (
            self.context['request'].user.is_authenticated
            and obj.shopping_list.filter(
                user=self.context['request'].user
            ).exists()
        )


class CreateAndUpdateRecipeSerializer(RecipeSerializer):
    """Сериализатор создания и обновления рецепта."""
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = AmountIngredientSerializer(many=True)
    cooking_time = serializers.IntegerField(
        validators=(
            validators.MinValueValidator(
                MIN_VALUE_VALIDATOR,
                message='Время приготовления должно быть не менее 1.'
            ),
            validators.MaxValueValidator(
                MAX_VALUE_VALIDATOR,
                message='Превышен лимит времени приготовления.'
            )
        )
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def validate_image(self, value):
        """Проверка наличия изображения."""
        if not value:
            raise exceptions.ValidationError(
                'Нужно добавить фото рецепта.'
            )
        return value

    def validate(self, data):
        """Проверка пустых и одинаковых тегов, и ингридиентов."""
        tags = data.get('tags', None)
        ingredients = data.get('ingredients', None)
        if not tags:
            raise exceptions.ValidationError(
                'Нужно добавить тег рецепта.'
            )
        if len(tags) != len(set(tags)):
            raise exceptions.ValidationError(
                'У рецепта не может быть два одинаковых тега.'
            )
        if not ingredients:
            raise exceptions.ValidationError(
                'Нужно добавить ингридиент рецепта.'
            )
        ingredient_ids = [ingredient['id'] for ingredient in ingredients]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise exceptions.ValidationError(
                'У рецепта не может быть два одинаковых ингредиента.'
            )
        return data

    def ingredients_create(self, recipe, ingredients):
        """Создание записи AmountIngredient."""
        all_obj_amount = []
        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient = get_object_or_404(Ingredient, pk=ingredient['id'])
            obj_amount = AmountIngredient(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount
            )
            all_obj_amount.append(obj_amount)
        AmountIngredient.objects.bulk_create(all_obj_amount)

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        self.ingredients_create(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.set(tags)
        ingredients = validated_data.pop('ingredients')
        instance.ingredients.clear()
        self.ingredients_create(instance, ingredients)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serializer = RecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        )
        return serializer.data


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор избранного рецепта."""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = FavoriteRecipe
        fields = (
            'user',
            'recipe'
        )

        validators = [
            UniqueTogetherValidator(
                queryset=FavoriteRecipe.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт добавлен в избранное.'
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        recipe = instance.recipe
        return ShortRecipeSerializer(
            recipe,
            context={'request': request}
        ).data


class ShoppingListSerializer(serializers.ModelSerializer):
    """Сериализатор корзины покупок."""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ShoppingList
        fields = (
            'user',
            'recipe'
        )

        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingList.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт добавлен в корзину.'
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        recipe = instance.recipe
        return ShortRecipeSerializer(
            recipe,
            context={'request': request}
        ).data
