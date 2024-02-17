"""Модуль кастомных прав."""

from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Пользователь - это admin или superamin django."""

    def has_permission(self, request, view):
        """Пользователь - это admin или superamin django."""
        return request.user.is_authenticated and (
            request.user.role == 'admin'
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Пользователь - это admin. Если нет то только чтение."""

    def has_permission(self, request, view):
        """Пользователь - это admin. Если нет то только чтение."""
        return (
            request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated and (
                    request.user.is_superuser or request.user.role == 'admin'
                )
            )
        )


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """Пользователь - это автор объекта либо moderator/admin."""

    def has_object_permission(self, request, view, obj):
        """Пользователь - это автор объекта либо moderator/admin."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                obj.author == request.user
                or request.user.role in ('moderator', 'admin')
            )
        )


class IsUserOrIsModeratorOrIsAdmin(permissions.BasePermission):
    """Проверка прав.

    Пользователь - это аутентифицированный пользователь,
    модератор или админ.
    """

    def has_permission(self, request, view):
        """Проверка прав.

        Пользователь - это аутентифицированный пользователь,
        модератор или админ.
        """
        return (request.user.role == 'user'
                or request.user.role == 'moderator'
                or request.user.role == 'admin')
