from rest_framework import serializers
from .models import *

class OnboardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Onboarding
        fields = ['id', 'title', 'description', 'image']

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']

class SupportMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportMessage
        fields = ['id', 'user', 'subject', 'message', 'created_at']