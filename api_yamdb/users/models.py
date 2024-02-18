"""Модуль для переопределения модели User."""

from random import choice

from django.contrib.auth.models import AbstractUser
from django.db import models

CONFIRMATION_CODE_LENGTH = 16
CONFIRMATION_CODE_PATTERN = r"^[A-Za-z0-9]+$"

CHOICES = (
    ('user', 'Обычный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class ExtendedUser(AbstractUser):
    """Модель кастомного юзера."""

    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        'Пользовательская роль',
        max_length=16,
        choices=CHOICES,
        default='user',
        blank=True,
    )
    email = models.EmailField(max_length=254, unique=True)
    confirmation_code = models.CharField(
        max_length=16,
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        """Meta-клас. Задаёт сортировку по полю id."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        """Возвращает email в качестве главного поля пользователя."""
        return self.email

    def save(self, *args, **kwargs):
        """Генерирует код-подтверждение и создаёт пользователя."""
        if not self.confirmation_code:
            self.confirmation_code = ''.join(choice(CONFIRMATION_CODE_PATTERN) for _ in range(CONFIRMATION_CODE_LENGTH))
        super().save(*args, **kwargs)

    def get_full_name(self):
        """Для обработки электронной почты возвращаем username."""
        return self.username

    def get_short_name(self):
        """Аналогично методу get_full_name()."""
        return self.username
