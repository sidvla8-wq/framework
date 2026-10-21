# Задание 30,2
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from courses.models import Course, Lesson
from users.models import Payment

User = get_user_model()


class Command(BaseCommand):
    help = "Создаёт тестовые платежи"

    def handle(self, *args, **options):
        user1 = User.objects.first()
        user2 = User.objects.filter(pk__gt=1).first()
        course1 = Course.objects.first()
        lesson1 = Lesson.objects.first()

        if not all([user1, course1, lesson1]):
            self.stdout.write("Сначала создайте пользователей, курсы и уроки.")
            return

        Payment.objects.bulk_create(
            [
                Payment(
                    user=user1, paid_course=course1, amount=2500, method="transfer"
                ),
                Payment(user=user2, paid_lesson=lesson1, amount=300, method="cash"),
            ]
        )
        self.stdout.write(self.style.SUCCESS("Платежи созданы"))
