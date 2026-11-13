# from rest_framework import viewsets, generics
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django_filters import rest_framework as dj_filters
# from django.shortcuts import get_object_or_404
#
# from .models import Course, Lesson, Subscription
# from .serializers import CourseSerializer, LessonSerializer
# from users.permissions import IsModer, IsModerOrOwner  # <-- добавлен IsModerOrOwner
#
#
# class CourseViewSet(viewsets.ModelViewSet):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#
#     def get_permissions(self):
#         # Чтение — любому авторизованному
#         if self.action in ('list', 'retrieve'):
#             return [IsAuthenticated()]
#         # Создание/изменение — тоже авторизованным,
#
#         return [IsAuthenticated(), IsModerOrOwner()]
#
#
# class LessonListCreateView(generics.ListCreateAPIView):
#     queryset = Lesson.objects.all().select_related('owner', 'course')
#     serializer_class = LessonSerializer
#     filter_backends = [dj_filters.DjangoFilterBackend]
#     filterset_fields = ['course']
#     # Любой авторизованный может создать СВОЙ урок.
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Lesson.objects.all().select_related('owner', 'course')
#     serializer_class = LessonSerializer
#
#     def get_permissions(self):
#         # Чтение — любому авторизованному
#         if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
#             return [IsAuthenticated()]
#         # Изменение/удаление — модератор ИЛИ владелец (один класс вместо `|`)
#         return [IsAuthenticated(), IsModerOrOwner()]
#
#
# class ToggleSubscriptionView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         user = request.user
#         course_id = request.data.get('course_id')
#
#         if not course_id:
#             return Response(
#                 {'detail': 'Обязательно укажите course_id в теле запроса.'},
#                 status=400
#             )
#
#         course = get_object_or_404(Course, pk=course_id)
#         subs_item = Subscription.objects.filter(user=user, course=course)
#
#         if subs_item.exists():
#             subs_item.delete()
#             message = 'Подписка удалена'
#         else:
#             Subscription.objects.create(user=user, course=course)
#             message = 'Подписка добавлена'
#
#         return Response({'message': message})
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Course, Payment
from .serializers import PaymentSerializer
from .services.stripe_service import (
    create_checkout_session,
    create_stripe_price,
    create_stripe_product,
)


class CreatePaymentView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        course = serializer.validated_data["course"]
        user = self.request.user
        amount_cents = course.price * 100  # цена в копейках

        # 1. Создаём продукт в Stripe
        product = create_stripe_product(
            name=course.title,
            description=course.description or "Курс на платформе",
        )

        # 2. Создаём цену в Stripe
        price = create_stripe_price(
            product_id=product.id,
            unit_amount_cents=amount_cents,
            currency=settings.STRIPE_CURRENCY,
        )

        # 3. Создаём сессию оплаты
        success_url = "http://127.0.0.1:8000/payment/success"  # для теста
        cancel_url = "http://127.0.0.1:8000/payment/cancel"  # для теста

        session = create_checkout_session(
            price_id=price.id,
            success_url=success_url,
            cancel_url=cancel_url,
        )

        # 4. Сохраняем платёж в своей БД
        payment = Payment.objects.create(
            user=user,
            course=course,
            amount=amount_cents,
            currency=settings.STRIPE_CURRENCY,
            stripe_product_id=product.id,
            stripe_price_id=price.id,
            stripe_session_id=session.id,
            checkout_url=session.url,
            status="pending",
        )
        serializer.save(id=payment.id)  # передаём id в ответ
