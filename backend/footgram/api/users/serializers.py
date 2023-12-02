from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueTogetherValidator

from api.recipes.short_recipe_serializer import ShortRecipeSerializer
from users.models import Follow

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
            return obj.following.filter(
                user=self.context.get('request').user
            ).exists()
        return False


class OutUserSerializer(CustomUserSerializer):
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
            'recipes',
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


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Follow
        fields = (
            'user',
            'author'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author'),
                message='одписка на автора выполнена!'
            )
        ]

    def validate(self, data):
        user = data['user']
        author = data['author']
        if author == user:
            raise exceptions.ValidationError(
                'Недопустимо подписаться на себя.'
                )
        return data
