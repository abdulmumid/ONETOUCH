from django.urls import path
from .views import *

urlpatterns = [
    path('onboarding/', OnboardingListView.as_view()),
    path('faqs/', FAQView.as_view()),
    path('support/messages/', SupportMessageView.as_view()),
    path("mycar-profile/", MycarProfileView.as_view()),
]
