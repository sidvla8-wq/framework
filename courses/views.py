from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as dj_filters
from django.shortcuts import get_object_or_404

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsModerOrOwner  # <-- добавлен IsModerOrOwner


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        # Чтение — любому авторизованному
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated()]
        # Создание/изменение — тоже авторизованным,
        # "модератор или владелец" проверяется на уровне объекта
        return [IsAuthenticated(), IsModerOrOwner()]


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all().select_related('owner', 'course')
    serializer_class = LessonSerializer
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_fields = ['course']
    # Любой авторизованный может создать СВОЙ урок.
    # Раньше стоял IsModer — это запрещало создавать уроки всем, кроме модераторов.
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all().select_related('owner', 'course')
    serializer_class = LessonSerializer

    def get_permissions(self):
        # Чтение — любому авторизованному
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return [IsAuthenticated()]
        # Изменение/удаление — модератор ИЛИ владелец (один класс вместо `|`)
        return [IsAuthenticated(), IsModerOrOwner()]


class ToggleSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {'detail': 'Обязательно укажите course_id в теле запроса.'},
                status=400
            )

        course = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

        return Response({'message': message})
