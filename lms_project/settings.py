INSTALLED_APPS = [
    "rest_framework",
    "users",
    "courses",  # приложение для курсов и уроков
    "django_filters",  # 4 задание фильтрация списков платежей ДХ 30,2
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",  # без авторизациипо заданию
    ],
}

AUTH_USER_MODEL = "users.User"
