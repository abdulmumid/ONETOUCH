from django.shortcuts import render
<<<<<<< HEAD:api/views.py
from rest_framework import generics
from .models import Onboarding, FAQ, SupportMessage
from .serializers import OnboardingSerializer, FAQSerializer, SupportMessageSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
import telebot
import os 
from dotenv import load_dotenv

load_dotenv()
=======
from rest_framework import generics, permissions, status
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny
from apps.user.permissions import IsEmailVerified
>>>>>>> f1e4b04 (apps):apps/main/views.py

class OnboardingListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Onboarding.objects.all()
    serializer_class = OnboardingSerializer


class FAQView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class SupportMessageView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SupportMessage.objects.all()
    serializer_class = SupportMessageSerializer

<<<<<<< HEAD:api/views.py
    def perform_create(self, serializer):
        instance = serializer.save()
        self.send_telegram_notification(instance)

    def send_telegram_notification(self, message):
        bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
        try:
            bot.send_message(
                chat_id=os.getenv('TELEGRAM_CHAT_ID'),
                text=(
                    f"Новое сообщение поддержки:\n\n"
                    f"Пользователь: {message.user.email}\n"
                    f"Тема: {message.subject}\n"
                    f"Сообщение: {message.message}"
                )
            )
        except Exception as e:
            print("Не удалось отправить уведомление в Telegram:", e)
=======

class MycarProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = MycarProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmailVerified]

    def get_object(self):
        profile, created = MycarProfile.objects.get_or_create(user=self.request.user)
        return profile
>>>>>>> f1e4b04 (apps):apps/main/views.py
