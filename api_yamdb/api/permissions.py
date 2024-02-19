"""Модуль кастомных прав."""

from rest_framework import permissions

from reviews.models import User

<<<<<<< HEAD
USER = 0
MODERATOR = 1
ADMIN = 2
ROLE_INDEX = 0
=======
USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
>>>>>>> 1434d6ab2270f1c3fc1c49279ca16f4e943973fd


class IsAdmin(permissions.BasePermission):
    """Пользователь - это admin или superamin django."""

    def has_permission(self, request, view):
        """Пользователь - это admin или superamin django."""
        return request.user.is_authenticated and (
            request.user.role == User.CHOICES[ADMIN][ROLE_INDEX]
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(IsAdmin):
    """Пользователь - это admin. Если нет то только чтение."""

    def has_permission(self, request, view):
        """Пользователь - это admin. Если нет то только чтение."""
        return (
<<<<<<< HEAD
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
=======
            request.method in permissions.SAFE_METHODS or (
                super().has_permission(request, view)
            )
>>>>>>> 1434d6ab2270f1c3fc1c49279ca16f4e943973fd
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
<<<<<<< HEAD
                or request.user.role == User.CHOICES[ADMIN][ROLE_INDEX]
                or request.user.role == User.CHOICES[MODERATOR][ROLE_INDEX]
=======
                or request.user.role in (MODERATOR, ADMIN)
>>>>>>> 1434d6ab2270f1c3fc1c49279ca16f4e943973fd
            )
        )
