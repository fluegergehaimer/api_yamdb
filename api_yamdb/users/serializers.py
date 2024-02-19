"""Модуоь сериализаторов приложения users."""

import re

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

User = get_user_model()

USERNAME_LENGTH = 150
USERNAME_PATTERN = r'^[\w@.+-_]+$'
EMAIL_FILED_LENGTH = 254
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


class RegistrationSerializer(serializers.Serializer):
    """Сериализация регистрации и создания нового пользователя."""

    username = serializers.CharField(max_length=USERNAME_LENGTH)
    email = serializers.EmailField(max_length=EMAIL_FILED_LENGTH)

    def validate(self, data):
        """Валидация данных для создания пользователя."""
        username = data.get('username', None)

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

        if username == 'me':
            raise serializers.ValidationError(
                {
                    'username': [
                        'Использовать имя "me" в качестве username запрещено.'
                    ]
                }
            )

        #  Мало!
        #  Такое сообщение умеет делать штатный Джанго валидатор регулярок. Для такого свой не нужен.
        #  У своего сделайте сообщение полезнее.
        #  Пусть он перечислит (по одному разу) все недопустимые символы, найденные в нике.
        pattern = re.compile(USERNAME_PATTERN)
        if not pattern.findall(username):
            raise serializers.ValidationError(
                {
                    'username': [
                        'username не соответствует паттерну.'
                    ]
                }
            )

        return username

    def create(self, validated_data):
        """Создаёт пользователя."""
        return User.objects.create_user(**validated_data)


class AuthenticationSerializer(serializers.Serializer):
    """Сериализация проверки confirmation_code и отправки token."""

    username = serializers.CharField(
        max_length=USERNAME_LENGTH,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_LENGTH,
        required=True,
    )

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
