from django.urls import path
from .views import OnboardingListView

urlpatterns = [
    path('onboarding/', OnboardingListView.as_view()),
]
