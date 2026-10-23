# from rest_framework import generics, viewsets
#
# from .models import Course, Lesson
# from .serializers import CourseSerializer, LessonSerializer
#
#
# # Course: ViewSet (CRUD)
# class CourseViewSet(viewsets.ModelViewSet):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#
#
# # Lesson: Generic-классы (полный CRUD)
# class LessonListCreateView(generics.ListCreateAPIView):
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer
#
#
# class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer

# Задание 31

from django_filters import rest_framework as filters
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsModer, IsOwner  # <-- вот эти импорты решают ошибки

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().select_related("owner")
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action == "create":
            return [IsModer()]
        return [IsAuthenticated(), IsModer() | IsOwner()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all().select_related("owner", "course")
    serializer_class = LessonSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["course"]
    permission_classes = [IsAuthenticated, IsModer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all().select_related("owner", "course")
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ["GET", "HEAD", "OPTIONS"]:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsModer() | IsOwner()]
