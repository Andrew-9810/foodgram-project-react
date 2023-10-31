# from django.contrib import admin
#
# from .models import (
#     Ingredient, Tag, AmountIngredient, FavoriteRecipe, Recipe, ShoppingList
# )
#
#
# class IngredientAdmin(admin.ModelAdmin):
#     list_display = (
#         'name',
#         'measurement_unit'
#     )
#     list_filter = ('name',)
#     search_fields = ('name',)
#     empty_value_display = '-пусто-'
#
#
# admin.site.register(Ingredient, IngredientAdmin)
#
#
# class TagAdmin(admin.ModelAdmin):
#     list_display = (
#         'name',
#         'color',
#         'slug'
#     )
#     list_filter = ('name', 'color', 'slug')
#     search_fields = ('name',)
#     empty_value_display = '-пусто-'
#
#
# admin.site.register(Tag, TagAdmin)
#
#
# class AmountIngredientInline(admin.TabularInline):
#     model = AmountIngredient
#
#
# class RecipeAdmin(admin.ModelAdmin):
#     inlines = [
#         AmountIngredientInline,
#     ]
#     readonly_fields = ('in_favorites',)
#     list_display = (
#         'name',
#         'author',
#         'in_favorites'
#     )
#     list_filter = ('name', 'author', 'tags')
#     search_fields = ('name',)
#     filter_horizontal = ('tags',)
#     empty_value_display = '-пусто-'
#
#     def in_favorites(self, instance):
#         return instance.favorite_recipes.count()
#     in_favorites.short_description = 'добавлен в избранное'
#
#
# class ShoppingListAdmin(admin.ModelAdmin):
#     list_display = (
#         'user',
#         'recipe'
#     )
#     list_filter = ('user', 'recipe')
#     search_fields = ('user',)
#     empty_value_display = '-пусто-'
#
#
# class FavoriteAdmin(admin.ModelAdmin):
#     list_display = (
#         'user',
#         'recipe'
#     )
#     list_filter = ('user', 'recipe')
#     search_fields = ('user',)
#     empty_value_display = '-пусто-'
#
#
# admin.site.register(Recipe, RecipeAdmin)
# admin.site.register(FavoriteRecipe, FavoriteAdmin)
# admin.site.register(ShoppingList, ShoppingListAdmin)
