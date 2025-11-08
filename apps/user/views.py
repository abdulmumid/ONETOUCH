from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from .models import OTP,  Avatar
from .serializers import (
    RegisterSerializer, VerifyOTPSerializer, ResendOTPSerializer,
    LoginSerializer, ResetPasswordSerializer, ResetPasswordConfirmSerializer,
    UpdateUserSerializer, UserSerializer, PlayerIdSerializer, AvatarSerializer
)
from .permissions import IsEmailVerified
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth import get_user_model
import os
from dotenv import load_dotenv

load_dotenv()

User = get_user_model()

# ------------------- Отправка писем -------------------
def send_user_mail(subject, message, recipient):
    if recipient:
        backend = None if not getattr(settings, 'USE_CONSOLE_EMAIL', True) else 'django.core.mail.backends.console.EmailBackend'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
            connection=None
        )

# ------------------- Регистрация -------------------
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        otp = OTP.objects.filter(user=user, purpose="registration").order_by("-created_at").first()
        if otp:
            send_user_mail(
                "Ваш код подтверждения",
                f"Ваш код подтверждения: {otp.code}. Никому не передавайте этот код.",
                user.email
            )

        return Response(
            {"message": "Регистрация успешна! Проверьте номер для подтверждения.", "email": user.email},
            status=status.HTTP_201_CREATED
        )

# ------------------- Подтверждение OTP -------------------
class VerifyOTPView(generics.GenericAPIView):
    serializer_class = VerifyOTPSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Email подтверждён!",
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)

# ------------------- Повторная отправка OTP -------------------
class ResendOTPView(generics.GenericAPIView):
    serializer_class = ResendOTPSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        user = result['user']
        otp = result['otp']
        send_user_mail(
            "Ваш новый код подтверждения",
            f"Новый код подтверждения: {otp.code}. Никому не передавайте этот код.",
            user.email
        )
        return Response({"message": "Новый код отправлен на email"}, status=status.HTTP_200_OK)

# ------------------- Вход -------------------
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"]
        )

        if not user:
            return Response({"error": "Неверный email или пароль"}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_verified:
            return Response({"error": "Подтвердите email перед входом"}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Успешный вход",
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)

# ------------------- Обновление player_id -------------------
class UpdatePlayerIdView(generics.UpdateAPIView):
    serializer_class = PlayerIdSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmailVerified]

    def get_object(self):
        return self.request.user

# ------------------- Сброс пароля -------------------
class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        otp = OTP.objects.filter(user=user, purpose="reset_password").order_by("-created_at").first()
        if otp:
            send_user_mail(
                "Код для сброса пароля",
                f"Ваш код для сброса пароля: {otp.code}. Никому не передавайте этот код.",
                user.email
            )
        return Response({"message": "Код для сброса пароля отправлен на email"}, status=status.HTTP_200_OK)

# ------------------- Подтверждение нового пароля -------------------
class ResetPasswordConfirmView(generics.GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Пароль успешно изменён"}, status=status.HTTP_200_OK)

# ------------------- Профиль пользователя -------------------
class UserMeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmailVerified]

    def get_object(self):
        return self.request.user

class UserUpdateProfileView(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmailVerified]

    def get_object(self):
        return self.request.user

class UserDeleteAccountView(generics.DestroyAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmailVerified]

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        with transaction.atomic():
            OTP.objects.filter(user=instance).delete()
            instance.delete()


class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), os.getenv('GOOGLE_CLIENT_ID'))
            email = idinfo['email']
            user, created = User.objects.get_or_create(email=email, defaults={"username": email.split("@")[0]})
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        except ValueError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)



class AvatarView(generics.RetrieveUpdateAPIView):
    serializer_class = AvatarSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmailVerified]

    def get_object(self):
        avatar, created = Avatar.objects.get_or_create(user=self.request.user)
        return avatar