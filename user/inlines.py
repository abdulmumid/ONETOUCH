from django.contrib import admin
from .models import MycarProfile, Avatar
from reservation.models import UserSubscription

class MycarProfileInline(admin.StackedInline):
    model = MycarProfile
    extra = 0

class AvatarInline(admin.StackedInline):
    model = Avatar
    extra = 0

class UserSubscriptionInline(admin.StackedInline):
    model = UserSubscription
    extra = 0