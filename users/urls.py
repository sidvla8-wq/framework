from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet, RegisterView, UserProfileView, UserProfileViewSet

router = DefaultRouter()
router.register(r"users", UserProfileViewSet, basename="user")
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", UserProfileView.as_view(), name="profile-me"),
]
