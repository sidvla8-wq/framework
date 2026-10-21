from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("courses.urls")),
    path("api/courses/", include("courses.urls")),
    path("api/users/", include("users.urls")),
]
