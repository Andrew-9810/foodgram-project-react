import rest_framework
from api.tags.serializers import TagSerializer
from api.users.serializers import CustomUserSerializer
from django.conf import settings
from django.core import validators
from django.http import Http404
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from recipes import models


class AmountIngredientSerializer(rest_framework.serializers.ModelSerializer):
    """Сериализатор количества ингредиентов в рецепте."""
    id = rest_framework.serializers.IntegerField()
    amount = rest_framework.serializers.IntegerField(
        validators=(
            validators.MinValueValidator(
                settings.MIN_VALUE_VALIDATOR,
                message='Количество ингредиентов должно быть не менее 1.'
            ),
            validators.MaxValueValidator(
                settings.MAX_VALUE_VALIDATOR,
                message='Превышен лимит количества ингредиентов.'
            )
        )
    )

    class Meta:
        model = models.AmountIngredient
        fields = ('id', 'amount')


class FullAmountIngredientSerializer(
    rest_framework.serializers.ModelSerializer
):
    """Сериализатор Суммы Ингридиетов."""
    id = rest_framework.serializers.IntegerField(source='ingredient.id')
    name = rest_framework.serializers.CharField(source='ingredient.name')
    measurement_unit = rest_framework.serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = models.AmountIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(rest_framework.serializers.ModelSerializer):
    """Сериализатор Рецептов."""
    is_favorited = rest_framework.serializers.SerializerMethodField()
    is_in_shopping_cart = rest_framework.serializers.SerializerMethodField()
    ingredients = rest_framework.serializers.SerializerMethodField()
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = models.Recipe
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
        ingredients = models.AmountIngredient.objects.filter(recipe=obj)
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
    tags = rest_framework.serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Tag.objects.all()
    )
    ingredients = AmountIngredientSerializer(many=True)
    cooking_time = rest_framework.serializers.IntegerField(
        validators=(
            validators.MinValueValidator(
                settings.MIN_VALUE_VALIDATOR,
                message='Время приготовления должно быть не менее 1.'
            ),
            validators.MaxValueValidator(
                settings.MAX_VALUE_VALIDATOR,
                message='Превышен лимит времени приготовления.'
            )
        )
    )

    class Meta:
        model = models.Recipe
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

    def validate_tags(self, value):
        """Проверка выбора тега."""
        if not value:
            raise rest_framework.exceptions.ValidationError(
                'Нужно добавить хотя бы один тег.'
            )
        if len(value) != len(set(value)):
            raise rest_framework.exceptions.ValidationError(
                'У рецепта не может быть два одинаковых тега.'
            )
        return value

    def validate_ingredients(self, value):
        """Проверка выбора одинаковых ингредиетов."""
        if not value:
            raise rest_framework.exceptions.ValidationError(
                'Нужно добавить хотя бы один ингредиент.'
            )
        ingredients = []
        for item in value:
            ingredients.append(item['id'])
        if len(ingredients) != len(set(ingredients)):
            raise rest_framework.exceptions.ValidationError(
                'У рецепта не может быть два одинаковых ингредиента.'
            )
        return value

    def validate_image(self, value):
        """Проверка наличия изображения."""
        if not value:
            raise rest_framework.exceptions.ValidationError(
                'Нужно добавить фото рецепта.'
            )
        return value

    def validate(self, data):
        tags = data.get('tags', None)
        ingredients = data.get('ingredients', None)
        if tags is None:
            raise rest_framework.exceptions.ValidationError(
                'Нужно добавить тег рецепта.'
            )
        if ingredients is None:
            raise rest_framework.exceptions.ValidationError(
                'Нужно добавить ингридиент рецепта.'
            )
        return data

    def ingredients_create(self, recipe, ingredients):
        """Создание ингредиентов."""
        all_obj_amount = []
        for ingredient in ingredients:
            amount = ingredient['amount']
            try:
                ingredient = get_object_or_404(models.Ingredient, pk=ingredient['id'])
            except Http404:
                raise rest_framework.exceptions.ValidationError(
                    'Указан несуществующий ингредиент.'
                )

            obj_amount = models.AmountIngredient(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount
            )
            all_obj_amount.append(obj_amount)
        models.AmountIngredient.objects.bulk_create(all_obj_amount)

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = models.Recipe.objects.create(author=author, **validated_data)
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
