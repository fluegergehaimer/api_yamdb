"""Модуль кастомных прав."""

from rest_framework import permissions

from reviews.models import User

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


class IsAdmin(permissions.BasePermission):
    """Пользователь - это admin или superamin django."""

    def has_permission(self, request, view):
        """Пользователь - это admin или superamin django."""
        return request.user.is_authenticated and (
            request.user.role == ADMIN
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(IsAdmin):
    """Пользователь - это admin. Если нет то только чтение."""

    def has_permission(self, request, view):
        """Пользователь - это admin. Если нет то только чтение."""
        return (
            request.method in permissions.SAFE_METHODS or (
                super().has_permission(request, view)
            )
        )


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """Пользователь - это автор объекта либо moderator/admin."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Пользователь - это автор объекта либо moderator/admin."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                obj.author == request.user
                or request.user.role in (MODERATOR, ADMIN)
            )
        )
