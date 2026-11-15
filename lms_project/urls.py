from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


ROOT_URLCONF = 'lms_project.urls'

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("api/users/", include("users.urls")),
    path('api/', include('courses.urls')),
    path("api/courses/", include("courses.urls")),
    # Эндпоинты для JWT (доступны без авторизации)
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Документация OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Интерактивный Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
]
