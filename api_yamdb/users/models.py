"""Модуль для переопределения модели User."""

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from rest_framework.exceptions import ValidationError

USERNAME_LENGTH = 150
USERNAME_PATTERN = r'^[\w@.+-_]+$'
CONFIRMATION_CODE_LENGTH = 16
ROLE_FIELD_LENGTH = 9
EMAIL_FILED_LENGTH = 254

DEFAULT_ROLE = 'user'

CHOICES = (
    ('user', 'Обычный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


def validate_not_me(value):
    if value.lower() == 'me':
        raise ValidationError('Username cannot be "me".')


class ExtendedUser(AbstractUser):
    """Модель кастомного юзера."""

    username = models.CharField(
        max_length=USERNAME_LENGTH,
        unique=True,
        validators=(RegexValidator(regex=USERNAME_PATTERN), validate_not_me)
    )
    email = models.EmailField(
        max_length=EMAIL_FILED_LENGTH,
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
