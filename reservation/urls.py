from django.urls import path
from .views import CarWashViewSet, SubscriptionView, UserSubscriptionView, BookingViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'car-washes', CarWashViewSet, basename='carwash')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('subscriptions/', SubscriptionView.as_view()),
    path('user-subscriptions/', UserSubscriptionView.as_view()),
]

urlpatterns += router.urls
