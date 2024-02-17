"""Модуоь сериализаторов приложения users."""

import re

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели User."""

    class Meta:
        """Meta-класс."""

        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    """Для PATCH запроса к api/v1/users/me/."""

    class Meta:
        """Отключает запись в поле role."""

        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
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

            self.send_success_email(user_exists)
            data['is_user_exist'] = True
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
        pattern = re.compile('^[\\w.@+-]+\\Z')
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
        new_user = User.objects.create_user(**validated_data)
        self.send_success_email(new_user)
        return new_user

    def send_success_email(self, user):
        """Отправляет email с кодом подтверждения."""
        send_mail(
            subject='Регистрация',
            message=f'Поздравляем! '
                    f'Пользоваетель {user.get_full_name()} зарегистрирован.'
                    f'Ваш confirmation_code: {user.confirmation_code}',
            from_email='from@example.com',
            recipient_list=[user.email],
            fail_silently=True,
        )


class AuthenticationSerializer(serializers.ModelSerializer):
    """Сериализация проверки confirmation_code и отправки token."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        """Meta-класс."""

        model = User
        fields = ['username', 'confirmation_code']

    def get_access_token(self, user):
        """Генерирует JWT-токен."""
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return access_token

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

        access_token = self.get_access_token(user)

        data['token'] = access_token
        return data

    def to_representation(self, instance):
        """Переопределен для возврата только токена."""
        return {'token': instance['token']}
