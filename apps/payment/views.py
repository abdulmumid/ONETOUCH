from rest_framework import viewsets, generics
from .models import CarWash, Booking, Subscription, UserSubscription, Notification
from .serializers import CarWashSerializer, BookingSerializer, SubscriptionSerializer, UserSubscriptionSerializer, NotificationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny, IsAuthenticated


class CarWashViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = CarWash.objects.all()
    serializer_class = CarWashSerializer


class SubscriptionView(generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [AllowAny]


class UserSubscriptionView(generics.ListCreateAPIView):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
<<<<<<< HEAD:reservation/views.py
        return Booking.objects.filter(user=user)

class NotificationView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
=======

        if getattr(self, 'swagger_fake_view', False) or user.is_anonymous:
            return Booking.objects.none()

        return Booking.objects.filter(user=user)

>>>>>>> f1e4b04 (apps):apps/payment/views.py
