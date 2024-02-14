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
        default='юзер',
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username


User = get_user_model()
