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
    )


User = get_user_model()
