# from django.urls import include, path
# from rest_framework.routers import DefaultRouter
#
# from .views import UserProfileViewSet
#
# router = DefaultRouter()
# router.register(r"users", UserProfileViewSet, basename="user")
#
# urlpatterns = [
#     path("", include(router.urls)),
# ]
# Задание 30,2
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r"users", UserProfileViewSet, basename="user")
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
]
