import re

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CHOICES, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role',)


class UserUpdateSerializer(serializers.ModelSerializer):
    """Для PATCH запроса к api/v1/users/me/ """

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role',)
        read_only_fields = ("role",)


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации и создания нового пользователя. """

    class Meta:
        model = User
        fields = ['email', 'username']
        extra_kwargs = {
            'email': {'validators': []},
            'username': {'validators': []},
        }

    def validate(self, data):
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

            send_mail(
                subject='Регистрация',
                message=f'Поздравляем! Пользоваетель {user_exists.get_full_name()} зарегистрирован.'
                        f'Ваш confirmation_code: {user_exists.confirmation_code}',
                from_email='from@example.com',
                recipient_list=[user_exists.email],
                fail_silently=True,
            )
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

    def create(self, validated_data):
        new_user = User.objects.create_user(**validated_data)
        send_mail(
            subject='Регистрация',
            message=f'Поздравляем! Пользоваетель {new_user.get_full_name()} зарегистрирован.'
                    f'Ваш confirmation_code: {new_user.confirmation_code}',
            from_email='from@example.com',
            recipient_list=[new_user.email],
            fail_silently=True,
        )
        return new_user


class AuthenticationSerializer(serializers.ModelSerializer):
    """ Сериализация проверки confirmation_code и отправки token. """
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']

    def get_access_token(self, user):
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return access_token

    def validate(self, data):
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
        """Переопределен для возврата только токена. """
        return {'token': instance['token']}
