INSTALLED_APPS = [
    "rest_framework",
    "users",
    "courses",  # приложение для курсов и уроков
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",  # без авторизациипо заданию
    ],
}

AUTH_USER_MODEL = "users.User"
