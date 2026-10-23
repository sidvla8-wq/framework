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

from rest_framework import viewsets, generics, mixins
from django_filters import rest_framework as filters
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModer, IsOwner, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().select_related('owner')
    serializer_class = CourseSerializer

    def get_permissions(self):
        # Разрешаем:
        # - создание только модераторам
        # - просмотр/обновление/удаление: либо модератор, либо владелец
        if self.action == 'create':
            return [IsModer()]
        return [IsAuthenticated(), IsModer() | IsOwner()]

    def perform_create(self, serializer):
        # Автоматически ставим владельца
        serializer.save(owner=self.request.user)


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all().select_related('owner', 'course')
    serializer_class = LessonSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['course']

    permission_classes = [IsAuthenticated, IsModer]  # только модераторы могут создавать уроки

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all().select_related('owner', 'course')
    serializer_class = LessonSerializer

    def get_permissions(self):
        # Просмотр: все авторизованные
        # Обновление/удаление: модератор или владелец
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsModer() | IsOwner()]
