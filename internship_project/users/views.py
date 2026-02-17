from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserSerializer
from .trainee_serializers import TraineeSerializer
from .permissions import IsAdminExtended
from .services import get_trainees_for_user
from .models import CustomUser, Trainee

class UserViewSet(viewsets.ModelViewSet):
    """
    Управление пользователями. Только админ может создавать/редактировать.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminExtended]
    queryset = CustomUser.objects.all()


class LoginView(APIView):
    """
    Вход пользователя.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Вход пользователя",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "password"],
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: UserSerializer, 401: "Неверный логин или пароль"},
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"error": "Неверный логин или пароль"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = UserSerializer(user)
        return Response(serializer.data)


class TraineeViewSet(viewsets.ModelViewSet):
    """
    Управление стажёрами. Доступ зависит от роли пользователя.
    """
    serializer_class = TraineeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Trainee.objects.none()
        return get_trainees_for_user(self.request.user)
