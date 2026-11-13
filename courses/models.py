# from django.conf import settings
# from django.db import models
#
#
# class Course(models.Model):
#     title = models.CharField(max_length=255)
#     preview = models.ImageField(upload_to="course_previews/", blank=True, null=True)
#     description = models.TextField(blank=True)
#     owner = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses"
#     )
#
#     def __str__(self):
#         return self.title
#
#
# class Lesson(models.Model):
#     course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     preview = models.ImageField(upload_to="lesson_previews/", blank=True, null=True)
#     video_url = models.URLField(max_length=500)
#     owner = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lessons"
#     )
#
#     class Meta:
#         ordering = ["id"]
#
#     def __str__(self):
#         return f"{self.course.title} — {self.title}"
#
#
# # Задание 32,1
#
#
# class Subscription(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions"
#     )
#     course = models.ForeignKey(
#         "courses.Course", on_delete=models.CASCADE, related_name="subscribers"
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = (
#             "user",
#             "course",
#         )  # один пользователь — одна подписка на курс
#
#     def __str__(self):
#         return f"{self.user.email} — {self.course.title}"

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.PROTECT)
    amount = models.PositiveIntegerField(help_text="Цена в копейках")
    currency = models.CharField(max_length=3, default='rub')

    stripe_product_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_session_id = models.CharField(max_length=100, blank=True, null=True)
    checkout_url = models.URLField(blank=True, null=True)  # ссылка на оплату Stripe

    status = models.CharField(
        max_length=20,
        default='pending',
        choices=[
            ('pending', 'Ожидает оплаты'),
            ('paid', 'Оплачено'),
            ('cancelled', 'Отменено'),
            ('failed', 'Ошибка'),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
