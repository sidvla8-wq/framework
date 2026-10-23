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
# from django.urls import include, path
# from rest_framework.routers import DefaultRouter
#
# from .views import PaymentViewSet, UserProfileViewSet
#
# router = DefaultRouter()
# router.register(r"users", UserProfileViewSet, basename="user")
# router.register(r"payments", PaymentViewSet, basename="payment")
#
# urlpatterns = [
#     path("", include(router.urls)),
# ]
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer, UserProfileSerializer
from .permissions import IsOwnerOrReadOnly, IsModer


router = DefaultRouter()
router.register(r'users', UserProfileViewSet, basename='user')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/me/', UserProfileView.as_view(), name='profile-me'),
]

User = get_user_model()

# Регистрация — доступна всем
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Возвращаем сразу пару токенов (как будто пользователь сразу «вошёл»)
        from rest_framework_simplejwt.tokens import RefreshToken
        user = serializer.instance
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserProfileSerializer(user).data,
        }, status=status.HTTP_201_CREATED, headers=headers)


# Профиль: просмотр любого, редактирование только своего
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    # Для просмотра чужого профиля — убираем чувствительные данные в сериализаторе
    # (это делается через логику в permission или кастомный queryset)


    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == 'me' or pk is None:
            return self.request.user
        return super().get_object()
