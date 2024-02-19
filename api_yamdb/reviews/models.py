"""Модели."""

from django.contrib.auth.models import AbstractUser
from django.core.validators import (MinValueValidator,
                                    MaxValueValidator,
                                    RegexValidator)
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

MESSAGE_1 = 'Оценка не может быть ниже 1.'
MESSAGE_2 = 'Оценка не может быть выше 10.'
NAME_MAX_LENGTH = 256
SLUG_MAX_LENGTH = 50
TEXT_LIMIT = 20
USERNAME_LENGTH = 150
USERNAME_PATTERN = r'^[\w@.+-_]+$'
CONFIRMATION_CODE_LENGTH = 16
ROLE_FIELD_LENGTH = 9
EMAIL_FIELD_LENGTH = 254

DEFAULT_ROLE = 'user'


def validate_not_me(value):
    """Функция-валидатор. Проверяет, что username != me."""
    if value.lower() == 'me':
        raise ValidationError('Username cannot be "me".')


class User(AbstractUser):
    """Модель кастомного юзера."""

    CHOICES = (
        ('user', 'Обычный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )

    username = models.CharField(
        max_length=USERNAME_LENGTH,
        unique=True,
        validators=(RegexValidator(regex=USERNAME_PATTERN), validate_not_me)
    )
    email = models.EmailField(
        max_length=EMAIL_FIELD_LENGTH,
        unique=True
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        'Пользовательская роль',
        max_length=ROLE_FIELD_LENGTH,
        choices=CHOICES,
        default=DEFAULT_ROLE,
        blank=True,
    )
    confirmation_code = models.CharField(
        max_length=CONFIRMATION_CODE_LENGTH,
        blank=True,
        null=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        """Meta-клас. Задаёт сортировку по полю id."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        """Возвращает email в качестве главного поля пользователя."""
        return self.email


class NameSlugModel(models.Model):
    """Базовая модель."""

    name = models.CharField(
        verbose_name='Название',
        max_length=NAME_MAX_LENGTH,
    )
    slug = models.SlugField(
        verbose_name='slug',
        max_length=50,
        unique=True,
    )

    class Meta:
        """Class Meta."""

        abstract = True

    def __str__(self):
        """Функция __str__."""
        return self.name[:TEXT_LIMIT]


class Genre(NameSlugModel):
    """Модель жанра."""

    class Meta:
        """Class Meta."""

        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)


class Category(NameSlugModel):
    """Модель категории."""

    class Meta:
        """Class Meta."""

        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        verbose_name='Название',
        max_length=NAME_MAX_LENGTH,
    )
    year = models.SmallIntegerField(
        verbose_name='Год',
        validators=[
            MinValueValidator(1888),
            MaxValueValidator(timezone.now().year),
        ]
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр',
        related_name='title_genre'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='title_category'
    )

    class Meta:
        """Class Meta."""

        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('year', 'name')

    def __str__(self):
        """Функция __str__."""
        return self.name


class GenreTitle(models.Model):
    """Модель жанра произведения."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta:
        """Class Meta."""

        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'

    def __str__(self):
        """Функция __str__."""
        return f'{self.title} принадлежит жанру {self.genre}'


class Review(models.Model):
    """Модель отзыва."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Оставить отзыв.',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, MESSAGE_1),
            MaxValueValidator(10, MESSAGE_2)
        ],
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        """Class Meta."""

        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review'
            )
        ]

    def __str__(self):
        """Функция __str__."""
        return f'{self.text[:TEXT_LIMIT]}, {self.score}'


class Comment(models.Model):
    """Модель комментария."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        """Class Meta."""

        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        """Функция __str__."""
        return self.text[:TEXT_LIMIT]
