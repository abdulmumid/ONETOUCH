from rest_framework import serializers
from .models import CarWash, Booking, Subscription, UserSubscription, Notification

class CarWashSerializer(serializers.ModelSerializer):
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()

    class Meta:
        model = CarWash
        fields = ['id', 'name', 'phone', 'whatsapp', 'instagram', 'address',
                  'open_time', 'closing_time', 'rating', 'img', 'latitude', 'longitude']

    def get_latitude(self, obj):
        return obj.location.y if obj.location else None

    def get_longitude(self, obj):
        return obj.location.x if obj.location else None


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class UserSubscriptionSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer(read_only=True)

    class Meta:
        model = UserSubscription
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    user_subscription = UserSubscriptionSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"

    def create(self, validated_data):
        booking = Booking.objects.create(**validated_data)
        return booking


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"