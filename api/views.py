from django.shortcuts import render
from rest_framework import generics
from .models import Onboarding, FAQ, SupportMessage
from .serializers import OnboardingSerializer, FAQSerializer, SupportMessageSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
import telebot

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

    def perform_create(self, serializer):
        instance = serializer.save()
        self.send_telegram_notification(instance)

    def send_telegram_notification(self, message):
        bot = telebot.TeleBot("7948742472:AAEz9hwOzf3rKH07RLGOToYL7kJ9B0_1Cxg")
        try:
            bot.send_message(
                chat_id=5349154050,
                text=(
                    f"Новое сообщение поддержки:\n\n"
                    f"Пользователь: {message.user.email}\n"
                    f"Тема: {message.subject}\n"
                    f"Сообщение: {message.message}"
                )
            )
        except Exception as e:
            print("Не удалось отправить уведомление в Telegram:", e)
