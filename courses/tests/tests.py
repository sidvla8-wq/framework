from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from courses.models import Course

User = get_user_model()


class CoursesTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # 1. Создаём пользователя — владельца курса
        self.owner = User.objects.create_user(
            username='course_owner',
            password='password123',
            email='owner@example.com',
        )

        # 2. Принудительная авторизация: работает с любой схемой

        self.client.force_authenticate(user=self.owner)

        # 3. Создаём курс

        self.course = Course.objects.create(
            title='Тестовый курс',
            owner=self.owner,
            # price=1000,        # раскомментируй, если поле обязательное
            # status='draft',    # раскомментируй, если поле обязательное
        )

    def _assert_status(self, response, expected_code, test_name):
        """Безопасная проверка статуса: не падает на response.data при 404"""
        if response.status_code != expected_code:
            msg = f"{test_name}: ожидался {expected_code}, получен {response.status_code}"
            if hasattr(response, 'data'):
                msg += f". Данные: {response.data}"
            else:
                msg += f". Content: {getattr(response, 'content', b'')[:200]}"
            self.fail(msg)

    # Тест 1: получение курса по ID
    def test_get_course_detail(self):
        url = f'/api/courses/{self.course.id}/'
        response = self.client.get(url)
        self._assert_status(response, 200, "test_get_course_detail")


    # Тест 2: создание урока владельцем курса
    def test_create_lesson_by_owner(self):
        url = '/api/lessons/'
        data = {
            'title': 'Новый урок',
            'course': self.course.id,
            'video_url': 'https://youtube.com/watch?v=test',
        }
        response = self.client.post(url, data, format='json')
        self._assert_status(response, 201, "test_create_lesson_by_owner")

    # --- Тест 3: создание урока с невалидной ссылкой
    def test_create_lesson_with_invalid_link(self):
        url = '/api/lessons/'
        data = {
            'title': 'Урок с плохой ссылкой',
            'course': self.course.id,
            'video_url': 'not-a-valid-url',  # не URL вообще
        }
        response = self.client.post(url, data, format='json')
        self._assert_status(response, 400, "test_create_lesson_with_invalid_link")