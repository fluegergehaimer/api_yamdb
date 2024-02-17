"""Модуль конфигурацию приложения."""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Класс конфигурацию приложения."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
