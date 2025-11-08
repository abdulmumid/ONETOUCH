from django.contrib import admin
from .models import Avatar
from apps.payment.models import UserSubscription



class AvatarInline(admin.StackedInline):
    model = Avatar
    extra = 0

class UserSubscriptionInline(admin.StackedInline):
    model = UserSubscription
    extra = 0
