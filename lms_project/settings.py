INSTALLED_APPS = [
    "rest_framework",
    "users",
    "courses",  # приложение для курсов и уроков
    "django_filters",  # 4 задание фильтрация списков платежей ДХ 30,2
    'rest_framework',
    'django_filters',
    'users',
    'courses',
    'rest_framework_simplejwt', # Задание 31
]

# REST_FRAMEWORK = {
#     "DEFAULT_PERMISSION_CLASSES": [
#         "rest_framework.permissions.AllowAny",  # без авторизациипо заданию
#     ],
# }
#
# AUTH_USER_MODEL = "users.User"
# Задание 31

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # по умолчанию всё закрыто
    ],
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
