"""Модуль для переопределения модели User."""

import secrets

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


CHOICES = (
    'user',
    'moderator',
    'admin',
)


class CustomUser(AbstractUser):
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
            self.confirmation_code = secrets.token_urlsafe(16)
        super().save(*args, **kwargs)

    def get_full_name(self):
        """Для обработки электронной почты возвращаем username."""
        return self.username

    def get_short_name(self):
        """Аналогично методу get_full_name()."""
        return self.username


User = get_user_model()
