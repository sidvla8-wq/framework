from django.contrib import admin
# from django.urls import include, path
#
# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("api/", include("courses.urls")),
#     path("api/courses/", include("courses.urls")),
#     path("api/users/", include("users.urls")),
# ]
# Задание 31

from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/courses/', include('courses.urls')),

    # Эндпоинты для JWT (доступны без авторизации)
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
