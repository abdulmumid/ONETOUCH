from django.urls import path
from .views import CarWashViewSet, SubscriptionView, UserSubscriptionView, BookingViewSet

urlpatterns = [
    path("car-wash/", CarWashViewSet.as_view({'get': 'list'})),  
    path("sbscription/", SubscriptionView.as_view()),
    path("user-subscription/", UserSubscriptionView.as_view()),
    path("booking/", BookingViewSet.as_view({'get': 'list'})),  
]
