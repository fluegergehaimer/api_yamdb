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

    def create(self, validated_data):
        if validated_data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        new_user = User.objects.create_user(**validated_data)
        send_mail(
            subject='Регистрация',
            message=f'Поздравляем! Пользоваетель {new_user.get_full_name()} зарегистрирован.'
                    f'Ваш confirmation_code: {new_user.confirmation_code}',
            from_email='from@example.com',
            recipient_list=['to@example.com'],
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
