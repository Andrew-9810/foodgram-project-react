from django.contrib import admin

from .models import (
    Ingredient, Tag, AmountIngredient, FavoriteRecipe, Recipe, ShoppingList
)


class IngredientAdmin(admin.ModelAdmin):
    """Отображение модели Ингредиентов в панели администратора."""
    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


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
    """!!!!Отображение модели Ингредиентов в панели администратора."""
    model = AmountIngredient


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

    def in_favorites(self, instance):
        return instance.favorite_recipes.count()
    in_favorites.short_description = 'Добавлен в избранное'


class ShoppingListAdmin(admin.ModelAdmin):
    """Отображение модели Корзина в панели администратора."""
    list_display = (
        'user',
        'recipe'
    )
    list_filter = ('user', 'recipe')
    search_fields = ('user',)
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    """Отображение модели Избранное в панели администратора."""
    list_display = (
        'user',
        'recipe'
    )
    list_filter = ('user', 'recipe')
    search_fields = ('user',)
    empty_value_display = '-пусто-'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(FavoriteRecipe, FavoriteAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
