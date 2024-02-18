"""Модуль предвставлений для приложения users."""

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from . import permissions
from .serializers import (
    AuthenticationSerializer, RegistrationSerializer, UserSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы администратора с users."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdmin,)
    lookup_field = 'username'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    search_fields = ('username',)

    @action(
        detail=False,
        methods=('get', 'patch'),
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        """Обрабатывает GET И PATCH запросы к api/v1/users/me."""
        if request.method == 'GET':
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(role=request.user.role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class RegistrationAPIView(APIView):
    """Вьюсет для регистрации пользователей."""

    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """Обрабатывает POST запросы к api/v1/auth/signup/.

        Если данные не валидны возвращает ошибку.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not serializer.validated_data.get('is_user_exist', None):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class AuthenticationAPIView(APIView):
    """Вьюсет для аутентификации пользователей по коду подтверждения."""

    serializer_class = AuthenticationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """Обрабатывает POST запросы к api/v1/auth/token/.

        Если данные не валидны возвращает ошибку.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
