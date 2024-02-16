from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'admin'
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated and (
                    request.user.is_superuser or request.user.role == 'admin'
                )
            )
        )


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """Проверяет, что user - это автор объекта либо moderator/admin. """
        return (
            request.method in permissions.SAFE_METHODS
            or
            request.user.is_authenticated
            and (
                obj.author == request.user
                or request.user.role in ('moderator', 'admin')
            )
        )


class IsUserOrIsModeratorOrIsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.role == 'user'
                or request.user.role == 'moderator'
                or request.user.role == 'admin')
