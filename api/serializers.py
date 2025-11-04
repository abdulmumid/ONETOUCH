from rest_framework import serializers
from .models import *

class OnboardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Onboarding
        fields = ['id', 'title', 'description', 'image']