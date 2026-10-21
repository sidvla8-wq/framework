# from rest_framework import serializers
#
# from .models import Course, Lesson
#
#
# class CourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Course
#         fields = "__all__"
#
#
# class LessonSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Lesson
#         fields = "__all__"
# Задание 30,2

from rest_framework import serializers

from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    # Количество уроков — динамическое поле
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "title", "preview", "description", "lessons_count"]

    def get_lessons_count(self, obj):
        # obj — это экземпляр Course
        return obj.lessons.count()


# Задание 3 к ДЗ 30,2
class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)  # вложенный сериализатор

    class Meta:
        model = Course
        fields = ["id", "title", "preview", "description", "lessons_count", "lessons"]

    def get_lessons_count(self, obj):
        return obj.lessons.count()
