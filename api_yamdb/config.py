"""Файл настроек."""

USERNAME_LENGTH = 150
USERNAME_PATTERN = r'^[\w.@+-]+\Z'
CHAR_PATTERN = r'[\w.@+-]'
EMAIL_FIELD_LENGTH = 254
CONF_CODE_LENGTH = 16
URL_PROFILE_PREF = 'me'
NOT_APPLICABLE = "N/A"
MIN_RATING = 1
MAX_RATING = 10

HTTP_METHODS = ('get', 'post', 'patch', 'delete')
CONF_CODE_PATTERN = r'^[A-Za-z0-9]+$'
SERVER_EMAIL = 'from@example.com'

DEFAULT_ROLE = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
