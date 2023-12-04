from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.users.serializers import FollowSerializer, FollowListSerializer
from api.utils.paginators import PageLimitPaginator
from users.models import Follow

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Вьюсет Пользователя. Наследуем от djoser."""
    pagination_class = PageLimitPaginator

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        """Мои подписки."""
        queryset = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = FollowListSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True, methods=['POST'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, id):
        """Подписаться на пользователя."""
        get_object_or_404(User, id=id)
        serializer = FollowSerializer(
            data={'author': id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        """Отписаться от пользователя."""
        user = request.user
        author = get_object_or_404(User, id=id)
        if not Follow.objects.filter(user=user, author=author).exists():
            return Response(
                {'errors': 'Подписка не найдена!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Follow.objects.get(user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
