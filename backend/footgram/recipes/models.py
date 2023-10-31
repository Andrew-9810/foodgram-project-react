# from colorfield.fields import ColorField
# from django.db import models
# from django.contrib.auth import get_user_model
# from django.core.validators import MinValueValidator
#
# User = get_user_model()
#
#
# class Ingredient(models.Model):
#     name = models.CharField(
#         verbose_name='Ингредиент',
#         max_length=200
#     )
#     measurement_unit = models.CharField(
#         verbose_name='Единицы измерения ингредиента',
#         max_length=50
#     )
#
#     class Meta:
#         verbose_name = "Ингредиент"
#         verbose_name_plural = "Ингредиенты"
#         ordering = ['name']
#
#     def __str__(self):
#         return self.name
#
#
# class Tag(models.Model):
#     """Модель тегов."""
#     name = models.CharField(
#         verbose_name='Название',
#         max_length=50,
#         unique=True
#     )
#     color = ColorField(
#         verbose_name='Цвет',
#         unique=True
#     )
#     slug = models.SlugField(
#         unique=True,
#         verbose_name='Слаг'
#     )
#
#     class Meta:
#         verbose_name = "Тег"
#         verbose_name_plural = "Теги"
#
#     def __str__(self):
#         return self.name
#
#
# class Recipe(models.Model):
#     """Рецепты."""
#     author = models.ForeignKey(
#         User,
#         verbose_name='Автор',
#         on_delete=models.CASCADE,
#         related_name='recipes',
#     )
#     name = models.CharField(
#         verbose_name='Название',
#         max_length=200
#     )
#     image = models.ImageField(
#         verbose_name='Изображение',
#         upload_to='recipes/',
#     )
#     text = models.TextField(
#         verbose_name='Рецепт',
#     )
#     ingredients = models.ManyToManyField(
#         Ingredient,
#         through='AmountIngredient',
#         related_name='recipes',
#         verbose_name='Ингредиенты'
#     )
#     tags = models.ManyToManyField(
#         Tag,
#         related_name='recipes',
#         verbose_name='Тэги'
#     )
#     cooking_time = models.PositiveIntegerField(
#         # Значение не может быть меньше 1, иначе ошибка
#         validators=(MinValueValidator(1),),
#         verbose_name='Время приготовления'
#     )
#     pub_date = models.DateTimeField(
#         verbose_name='Дата создания',
#         auto_now_add=True
#     )
#
#     class Meta:
#         verbose_name = "Рецепт"
#         verbose_name_plural = "Рецепты"
#         ordering = ['-pub_date']
#
#     def __str__(self):
#         return self.name
#
#
# class AmountIngredient(models.Model):
#     """Количество ингоидеентов в рецепте."""
#     ingredient = models.ForeignKey(
#         Ingredient,
#         verbose_name='Название',
#         on_delete=models.CASCADE
#     )
#     amount = models.PositiveIntegerField(
#         # Значение не может быть меньше 1, иначе ошибка
#         validators=(MinValueValidator(1),),
#         verbose_name='Количество'
#     )
#     recipe = models.ForeignKey(
#         Recipe,
#         verbose_name='Рецепт',
#         on_delete=models.CASCADE,
#     )
#
#     class Meta:
#         verbose_name = "Колличество ингридиента в рецепте"
#         verbose_name_plural = "Колличество ингридиентов в рецепте"
#         ordering = ['ingredient']
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['ingredient', 'recipe'],
#                 name='unique_ingredient'
#             )
#         ]
#
#     def __str__(self):
#         return self.ingredient.name
#
#
# class FavoriteRecipe(models.Model):
#     """Избранные рецепты пользователя."""
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='favorite_recipes',
#         verbose_name='Автор рецепта'
#     )
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE,
#         related_name='favorite_recipes',
#         verbose_name='Рецепт'
#     )
#
#     class Meta:
#         verbose_name = "Рецепт"
#         verbose_name_plural = "Рецепты"
#         ordering = ['user']
#         # Уникальное поле модели
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['user', 'recipe'],
#                 name='unique_favorite_model'
#             )
#         ]
#
#     def __str__(self):
#         return f'{self.recipe} в избранном у {self.user}'
#
#
# class ShoppingList(models.Model):
#     """Корзина покупок."""
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='shopping_list_recipes',
#         verbose_name='Покупатель'
#     )
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE,
#         related_name='shopping_list_recipes',
#         verbose_name='Рецепт'
#     )
#
#     class Meta:
#         verbose_name = "Корзина"
#         verbose_name_plural = "Корзина"
#         ordering = ['user']
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['user', 'recipe'],
#                 name='unique_shopping_list_model'
#             )
#         ]
#
#     def __str__(self):
#         return f'{self.recipe} в корзине у {self.user}'
