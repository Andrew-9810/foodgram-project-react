from rest_framework import permissions


class IsOnwer(permissions.BasePermission):
    """Ограничение запроса users/me только владельцу."""
    def has_permission(self, request, view):
        if view.name != 'Me':
            return bool(
                request.method in permissions.SAFE_METHODS
                or request.user and request.user.is_authenticated
            )
        else:
            return bool(
                request.user and request.user.is_authenticated
            )


class OwnerOrReadOnly(permissions.BasePermission):
    """Ограничение изменениея объекта. Владелец или только чтение."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class ReadOnly(permissions.BasePermission):
    """Ограничение, только для чтения."""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
