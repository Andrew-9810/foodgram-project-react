from django.contrib import admin

from recipes.models import (
    AmountIngredient, FavoriteRecipe, Ingredient, Recipe, ShoppingList, Tag
)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Отображение модели Ингредиентов в панели администратора."""
    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Отображение модели Тег в панели администратора."""
    list_display = (
        'name',
        'color',
        'slug'
    )
    list_filter = ('name', 'color', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class AmountIngredientInline(admin.TabularInline):
    """Отображение модели Ингредиентов в панели администратора."""
    model = AmountIngredient
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Отображение модели Рецепты в панели администратора."""
    inlines = [
        AmountIngredientInline,
    ]
    readonly_fields = ('in_favorites',)
    list_display = (
        'name',
        'author',
        'in_favorites'
    )
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name',)
    filter_horizontal = ('tags',)
    empty_value_display = '-пусто-'

    @admin.display(description='Добавлений в избранное')
    def in_favorites(self, instance):
        return instance.favorite.count()


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    """Отображение модели Корзина в панели администратора."""
    list_display = (
        'user',
        'recipe'
    )
    list_filter = ('user', 'recipe')
    search_fields = ('user',)
    empty_value_display = '-пусто-'


@admin.register(FavoriteRecipe)
class FavoriteAdmin(admin.ModelAdmin):
    """Отображение модели Избранное в панели администратора."""
    list_display = (
        'user',
        'recipe'
    )
    list_filter = ('user', 'recipe')
    search_fields = ('user',)
    empty_value_display = '-пусто-'
