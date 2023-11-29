from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from footgram.settings import (
    MAX_LENGTH_50, MAX_LENGTH_200, MIN_VALUE_VALIDATOR, MAX_VALUE_VALIDATOR
)

User = get_user_model()


class Ingredient(models.Model):
    """Модель Ингредиентов."""
    name = models.CharField(
        verbose_name='Ингредиент',
        max_length=MAX_LENGTH_200
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения ингредиента',
        max_length=MAX_LENGTH_50
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ['name']

        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient_model'
            )
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель Теги."""
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_LENGTH_50,
        unique=True
    )
    color = ColorField(
        verbose_name='Цвет',
        format='hex',
        unique=True
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель Рецепты."""
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_LENGTH_200
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/',
    )
    text = models.TextField(
        verbose_name='Рецепт',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='AmountIngredient',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(MIN_VALUE_VALIDATOR),
            MaxValueValidator(MAX_VALUE_VALIDATOR)
        ),
        verbose_name='Время приготовления'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class AmountIngredient(models.Model):
    """Модель Количество ингридеентов в рецепте."""
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Название',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(MIN_VALUE_VALIDATOR),
            MaxValueValidator(MAX_VALUE_VALIDATOR)
        ),
        verbose_name='Количество'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Колличество ингридиента в рецепте"
        verbose_name_plural = "Колличество ингридиентов в рецепте"
        ordering = ['ingredient']
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return self.ingredient.name


class FavoriteRecipe(models.Model):
    """Модель Избранные рецепты пользователя."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Автор рецепта'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"
        ordering = ['user']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_model'
            )
        ]

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'


class ShoppingList(models.Model):
    """Модель Корзина покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Покупатель'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"
        ordering = ['user']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_list_model'
            )
        ]

    def __str__(self):
        return f'{self.recipe} в корзине у {self.user}'
