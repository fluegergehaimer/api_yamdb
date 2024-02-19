"""Модуль предвставлений для приложения users."""

from random import choice

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from . import permissions
from .serializers import (AuthenticationSerializer,
                          RegistrationSerializer,
                          UserSerializer,
                          UserUpdateSerializer)

User = get_user_model()

CONFIRMATION_CODE_LENGTH = 16
CONFIRMATION_CODE_PATTERN = r'^[A-Za-z0-9]+$'
SERVER_EMAIL = 'from@example.com'


def get_confirmation_code():
    return ''.join(
        choice(CONFIRMATION_CODE_PATTERN) for _ in range(CONFIRMATION_CODE_LENGTH)
    )


def send_success_email(user):
    """Отправляет email с кодом подтверждения."""
    send_mail(
        subject='Регистрация',
        message=f'Ваш confirmation_code: {user.confirmation_code}',
        from_email=SERVER_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )


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
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def go_users_profile(self, request):
        """Обрабатывает GET И PATCH запросы к api/v1/users/me."""
        if request.method == 'GET':
            return Response(UserSerializer(request.user).data)
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegistrationAPIView(APIView):
    """Вьюсет для регистрации пользователей."""

    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def get_user(self):
        return User.objects.filter(username=self.request.data.get('username'))

    def post(self, request):
        """Обрабатывает POST запросы к api/v1/auth/signup/.

        Если данные не валидны возвращает ошибку.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_exists = self.get_user()

        if not user_exists.first():
            serializer.save(confirmation_code=get_confirmation_code())
        else:
            #  PIN обновляется
            user_exists.update(confirmation_code=get_confirmation_code())

        send_success_email(user_exists.first())
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthenticationAPIView(APIView):
    """Вьюсет для аутентификации пользователей по коду подтверждения."""

    serializer_class = AuthenticationSerializer
    permission_classes = (AllowAny,)

    def get_user(self):
        return User.objects.filter(username=self.request.data.get('username'))

    def get_access_token(self, user):
        """Генерирует JWT-токен."""
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return access_token

    def post(self, request):
        """Обрабатывает POST запросы к api/v1/auth/token/.

        Если данные не валидны возвращает ошибку.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        #  PIN удаляется для невозможности использовать его ещё раз
        self.get_user().update(confirmation_code=None)

        return Response({
            'token': self.get_access_token(self.get_user().first())
        },
            status=status.HTTP_200_OK
        )
