"""Модуоь сериализаторов приложения users."""

import re

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

USERNAME_LENGTH = 150
CONFIRMATION_CODE_LENGTH = 16


class UserUserUpdateSerializer(serializers.ModelSerializer):
    """Базовая модель сериалайзера для модели User."""

    class Meta:
        """Meta-класс."""

        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        abstract = True


class UserSerializer(UserUserUpdateSerializer):
    """Сериалайзер для модели User."""

    class Meta(UserUserUpdateSerializer.Meta):
        """Meta-класс."""


class UserUpdateSerializer(UserUserUpdateSerializer):
    """Для PATCH запроса к api/v1/users/me/."""

    class Meta(UserUserUpdateSerializer.Meta):
        """Отключает запись в поле role."""

        read_only_fields = ('role',)


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализация регистрации и создания нового пользователя."""

    class Meta:
        """Отключение пред-валидации полей email и username."""

        model = User
        fields = ['email', 'username']
        extra_kwargs = {
            'email': {'validators': []},
            'username': {'validators': []},
        }

    def validate(self, data):
        """Валидация данных для создания пользователя."""
        username = data.get('username', None)

        if username == 'me':
            raise serializers.ValidationError(
                {
                    'username': [
                        'Использовать имя "me" в качестве username запрещено.'
                    ]
                }
            )

        user_exists = User.objects.filter(username=username).first()

        if user_exists:
            if data.get('email') != user_exists.email:
                raise serializers.ValidationError(
                    {
                        'email': [
                            'Нельзя изменить почту.'
                        ]
                    }
                )

            return data

        # Если пользователя нет в базе - проверяем не занят ли email
        email = data.get('email', None)
        if User.objects.filter(email=email):
            raise serializers.ValidationError(
                {
                    'email': [
                        'email уже используется.'
                    ]
                }
            )

        return data

    def validate_username(self, username):
        """Валидауия поля username."""
        pattern = re.compile('^[\w.@+-]+\Z')
        if not pattern.findall(username):
            raise serializers.ValidationError(
                {
                    'username': [
                        'username не соответствует паттерну.'
                    ]
                }
            )

        return username


class AuthenticationSerializer(serializers.ModelSerializer):
    """Сериализация проверки confirmation_code и отправки token."""

    username = serializers.CharField(
        max_length=USERNAME_LENGTH,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_LENGTH,
        required=True,
    )

    class Meta:
        """Meta-класс."""

        model = User
        fields = ['username', 'confirmation_code']

    # def get_access_token(self, user):
    #     """Генерирует JWT-токен."""
    #     refresh = RefreshToken.for_user(user)
    #     access_token = str(refresh.access_token)
    #     return access_token

    def validate(self, data):
        """Валидация кода-подтверждения.

        Если код валиден - в словарь data добавляется JWT-токен.
        """
        user = get_object_or_404(User, username=data.get('username'))
        confirmation_code = data.get('confirmation_code')

        if confirmation_code != user.confirmation_code:
            raise serializers.ValidationError(
                'Отсутствует обязательное поле или оно некорректно'
            )

        return data
