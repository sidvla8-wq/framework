from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import UserProfileSerializer

User = get_user_model()

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    # По заданию не закрываем доступ
    