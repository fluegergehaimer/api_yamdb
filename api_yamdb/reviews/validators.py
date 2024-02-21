import re

from django.core.exceptions import ValidationError

from config import URL_PROFILE_PREF, USERNAME_PATTERN, CHAR_PATTERN, NOT_APPLICABLE


def validate_not_me(username):
    """Функция-валидатор. Проверяет, что username != me."""
    if username == URL_PROFILE_PREF:
        raise ValidationError(
                {
                    'username': [
                        f'Использовать имя "{URL_PROFILE_PREF}" в качестве username запрещено.'
                    ]
                }
            )


def validate_username_via_regex(username):
    """Валидауия поля username."""

    if not re.match(USERNAME_PATTERN, username):
        difference = set(username) - set(re.findall(CHAR_PATTERN, username))
        raise ValidationError(
            {
                'username': [
                    f'Недопустимые символы в username: '
                    f'{difference}'
                ]
            }
        )


def validate_confirmation_code(confirmation_code):
    """Валидауия поля username."""
    if confirmation_code == NOT_APPLICABLE:
        raise ValidationError(
            {
                "Отсутствует обязательное поле или оно некорректно"
            }
        )
