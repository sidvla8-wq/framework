# from django.urls import include, path
# from rest_framework.routers import DefaultRouter
#
# from .views import CourseViewSet, LessonDetailView, LessonListCreateView
#
# router = DefaultRouter()
# router.register(r"courses", CourseViewSet, basename="course")
#
# urlpatterns = [
#     path("", include(router.urls)),
#     path("lessons/", LessonListCreateView.as_view(), name="lesson-list-create"),
#     path("lessons/<int:pk>/", LessonDetailView.as_view(), name="lesson-detail"),
# ]

# Задание 31

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreateView, LessonDetailView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
]