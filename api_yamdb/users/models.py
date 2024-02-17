import secrets

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


CHOICES = (
    ('anonymous', 'аноним'),
    ('user', 'юзер'),
    ('moderator', 'модератор'),
    ('admin', 'админ'),
    ('superadmin', 'суперадмин'),
)


class CustomUser(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        'Пользовательская роль',
        max_length=16,
        choices=CHOICES,
        default='user',
        blank=True
    )
    email = models.EmailField(max_length=254, unique=True)
    confirmation_code = models.CharField(
        max_length=16,
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.confirmation_code:
            self.confirmation_code = secrets.token_urlsafe(16)
        super().save(*args, **kwargs)

    def get_full_name(self):
        """Для обработки электронной почты возвращаем username. """
        return self.username

    def get_short_name(self):
        """ Аналогично методу get_full_name(). """
        return self.username


User = get_user_model()
