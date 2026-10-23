# from django.contrib.auth import get_user_model
# from rest_framework import viewsets
#
# from .serializers import UserProfileSerializer
#
# User = get_user_model()
#
#
# class UserProfileViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserProfileSerializer
#     # По заданию не закрываем доступ
# Задание 30,2 ViewSet и фильтрация

from django_filters import rest_framework as filters
from rest_framework import viewsets

from .models import Payment
from .serializers import PaymentSerializer


class PaymentFilter(filters.FilterSet):
    course = filters.NumberFilter(field_name="paid_course__id")
    lesson = filters.NumberFilter(field_name="paid_lesson__id")
    method = filters.CharFilter(field_name="method")

    class Meta:
        model = Payment
        fields = []


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().select_related(
        "user", "paid_course", "paid_lesson"
    )
    serializer_class = PaymentSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PaymentFilter
    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]  # по умолчанию — новые сверху
