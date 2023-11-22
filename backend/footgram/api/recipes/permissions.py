from rest_framework import permissions


SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsOnwer(permissions.BasePermission):
    """Запрос users/me только владельцу."""
    def has_permission(self, request, view):
        if view.name != 'Me':
            return bool(
                request.method in SAFE_METHODS or
                request.user and
                request.user.is_authenticated
            )
        else:
            return bool(
                request.user and request.user.is_authenticated
            )
