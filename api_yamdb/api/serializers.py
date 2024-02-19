"""Сериалайзеры."""

import re

from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment, User

USERNAME_LENGTH = 150
USERNAME_PATTERN = r'^[\w@.+-_]+$'
EMAIL_FILED_LENGTH = 254
CONFIRMATION_CODE_LENGTH = 16
MIN_RATING = 1
MAX_RATING = 10


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        """Class Meta."""

        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        """Class Meta."""

        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        """Class Meta."""

        model = Title
        fields = ('id', 'category', 'genre', 'name',
                  'year', 'rating', 'description')


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор создания и обновления произведений."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=True
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=True
    )

    class Meta:
        """Class Meta."""

        model = Title
        fields = ('id', 'name', 'year', 'genre', 'category', 'description')
        read_only_fields = ('rating',)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    score = serializers.IntegerField(
        validators=[
            MinValueValidator(MIN_RATING),
            MaxValueValidator(MAX_RATING)
        ]
    )

    class Meta:
        """Class Meta."""

        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """Функция проверки данных."""
        if self.context['request'].method != 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title__id=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на данное произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        """Class Meta."""

        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


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

        invalid_characters = []
        for char in username:
            if not re.search(USERNAME_PATTERN, char):
                invalid_characters.append(char)
        if invalid_characters:
            raise serializers.ValidationError(
                {
                    'username': [
                        f'Недопустимые символы в username: '
                        f'{", ".join(invalid_characters)}'
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
