# from django.contrib.auth import get_user_model
# from rest_framework import serializers
#
# User = get_user_model()
#
#
# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "email", "phone", "city", "avatar"]
#         read_only_fields = ["email"]
# Задание 30,2
# from django.contrib.auth import get_user_model
# from rest_framework import serializers
#
# from .models import Payment
#
# User = get_user_model()
#
#
# class PaymentSerializer(serializers.ModelSerializer):
#     user_email = serializers.EmailField(source="user.email", read_only=True)
#     course_title = serializers.CharField(
#         source="paid_course.title", read_only=True, allow_null=True
#     )
#     lesson_title = serializers.CharField(
#         source="paid_lesson.title", read_only=True, allow_null=True
#     )
#
#     class Meta:
#         model = Payment
#         fields = [
#             "id",
#             "user",
#             "user_email",
#             "paid_course",
#             "course_title",
#             "paid_lesson",
#             "lesson_title",
#             "amount",
#             "payment_date",
#             "method",
#         ]
#         read_only_fields = ["user_email", "course_title", "lesson_title"]
#
#
# # Доп задание для ДЗ 30,2
#
#
# class UserProfileSerializer(serializers.ModelSerializer):
#     payments = PaymentSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = User
#         fields = ["id", "email", "phone", "city", "avatar", "payments"]
#         read_only_fields = ["email"]
# Задание 31

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Course, Lesson, Payment

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "phone", "city", "avatar"]

    def create(self, validated_data):
        avatar = validated_data.pop("avatar", None)
        user = User.objects.create_user(**validated_data)
        if avatar:
            user.avatar = avatar
            user.save()
        return user


class PaymentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    course_title = serializers.CharField(
        source="paid_course.title", read_only=True, allow_null=True
    )
    lesson_title = serializers.CharField(
        source="paid_lesson.title", read_only=True, allow_null=True
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "user_email",
            "paid_course",
            "course_title",
            "paid_lesson",
            "lesson_title",
            "amount",
            "payment_date",
            "method",
        ]
        read_only_fields = ["user_email", "course_title", "lesson_title"]


class UserProfileSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "phone", "city", "avatar", "payments"]
        read_only_fields = ["email"]


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "preview",
            "description",
            "owner",
            "lessons_count",
            "lessons",
        ]

    def get_lessons_count(self, obj):
        return obj.lessons.count()
