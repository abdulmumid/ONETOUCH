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

<<<<<<< HEAD:api/serializers.py
=======
class MycarProfileSerializer(serializers.ModelSerializer):
    marka = serializers.StringRelatedField()  
    model = serializers.StringRelatedField()  
    body = serializers.StringRelatedField()   

    class Meta:
        model = MycarProfile
        fields = ['id', 'user', 'marka', 'model', 'body', 'gos_number']
        read_only_fields = ['user']
>>>>>>> f1e4b04 (apps):apps/main/serializers.py
