from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'admin'


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
                request.user.role == 'admin')


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Проверяет, что user - это автор объекта либо moderator/admin. """
        return (obj.author == request.user
                or request.user.role in ('moderator', 'admin'))
