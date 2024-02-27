"""Файл настроек."""

import string

USERNAME_LENGTH = 150
USERNAME_INVALID_PATTERN = r'[^\w.@+-]'
EMAIL_FIELD_LENGTH = 254
CONF_CODE_LENGTH = 16
URL_PROFILE_PREF = 'me'
NOT_APPLICABLE = 'N/A'
MIN_RATING = 1
MAX_RATING = 10
CONF_CODE_LENGTH = 16

HTTP_METHODS = ('get', 'post', 'patch', 'delete')
CONF_CODE_PATTERN = string.ascii_letters + string.digits
SERVER_EMAIL = 'from@example.com'
