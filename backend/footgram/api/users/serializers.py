from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import Recipe

User = get_user_model()


class CustomCreateUserSerializer(UserCreateSerializer):
    """Сериализатор добавления пользователя, унаследовано от djoser."""
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        )


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователя, унаследовано от djoser."""
    # Вычисляемое поле подписок
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        """Вычисляем подписан ли текущий пользователь
         (от имени которого производися запрос)
         на пользователя по которому производим запрос."""

        if self.context.get('request').user.is_authenticated:
            # если Пользователь аутендефицирован то обращаемся по related_name к  модели подписок
            # в качестве obj выступает пользователь по которому производим запрос
            # в качестве user выступает текущий пользователь
            # Существует ли запись где автор Вася Пупкин, а подписчик Тест
            return obj.following.filter(
                user=self.context.get('request').user
            ).exists()
        return False


class FollowSerializer(CustomUserSerializer):
    """Сериализатор подписок."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            # Список объектов текущей страницы
            'recipes',
            # Общее количество объектов в базе
            'recipes_count'
        )

    def get_recipes(self, obj):
        """Получение объекта рецепта."""
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        queryset = obj.recipes.all()
        if recipes_limit:
            queryset = queryset[:int(recipes_limit)]
        return ShortRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        """Получение колличесва рецептов."""
        return obj.recipes.count()


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Рецепты автора, сокращеннный вариант."""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
