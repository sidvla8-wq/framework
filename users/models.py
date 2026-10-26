# from django.contrib.auth.models import AbstractUser
# from django.db import models
#
#
# class User(AbstractUser):
#     username = None  # отключаем username
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     city = models.CharField(max_length=100, blank=True, null=True)
#     avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
#
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []  # password обязателен по умолчанию
#
#     def __str__(self):
#         return self.email
# Задание 30,2
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import SET_NULL

User = get_user_model()


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счёт"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    paid_course = models.ForeignKey(
        "courses.Course",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="course_payments",
    )
    paid_lesson = models.ForeignKey(
        "courses.Lesson",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="lesson_payments",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)

    def clean(self):
        from django.core.exceptions import ValidationError

        if not self.paid_course and not self.paid_lesson:
            raise ValidationError("Нужно указать либо курс, либо урок.")
        if self.paid_course and self.paid_lesson:
            raise ValidationError(
                "Можно оплатить либо курс, либо отдельный урок, но не оба сразу."
            )

    def __str__(self):
        return f"{self.user.email} — {self.amount} ({self.method})"
