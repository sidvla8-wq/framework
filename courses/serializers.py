from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from rest_framework import serializers

from .models import Course, Lesson, Subscription


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ("owner",)


class LessonSerializer(serializers.ModelSerializer):
    # owner заполняется автоматически из request.user
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Lesson
        fields = "__all__"

    def validate_video_url(self, value):
        """Ссылка на видео должна быть валидным http/https URL"""
        validator = URLValidator(schemes=["http", "https"])
        try:
            validator(value)
        except ValidationError:
            raise serializers.ValidationError(
                "Ссылка должна быть валидным URL (http/https)."
            )
        return value


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
        read_only_fields = ("user",)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "course", "amount", "currency", "checkout_url", "status"]
        read_only_fields = ["amount", "currency", "checkout_url", "status"]
