from django.shortcuts import render
from rest_framework import generics
from .models import Onboarding
from .serializers import OnboardingSerializer
from rest_framework.permissions import AllowAny

class OnboardingListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Onboarding.objects.all()
    serializer_class = OnboardingSerializer