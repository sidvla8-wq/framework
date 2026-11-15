from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, PaymentCreateAPIView, PaymentStatusAPIView

router = DefaultRouter()
router.register(r"courses", CourseViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payment-create"),
    path(
        "payments/<int:pk>/status/",
        PaymentStatusAPIView.as_view(),
        name="payment-status",
    ),
]