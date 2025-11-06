from django.shortcuts import render
from rest_framework import generics
from .models import Onboarding, FAQ, SupportMessage
from .serializers import OnboardingSerializer, FAQSerializer, SupportMessageSerializer
from rest_framework.permissions import AllowAny

class OnboardingListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Onboarding.objects.all()
    serializer_class = OnboardingSerializer


class FAQView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class SupportMessageView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = SupportMessage.objects.all()
    serializer_class = SupportMessageSerializer