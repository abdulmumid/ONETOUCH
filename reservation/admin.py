from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import CarWash, Booking, Subscription, UserSubscription, Notification
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(CarWash)
class CarWashAdmin(LeafletGeoAdmin):
    list_display = ('name', 'phone', 'address', 'open_time', 'closing_time', 'rating', 'show_whatsapp', 'show_instagram')
    search_fields = ('name', 'address', 'phone')
    list_filter = ('rating',)
    settings_overrides = {
        'DEFAULT_CENTER': (42.87, 74.59),
        'DEFAULT_ZOOM': 12,
    }

    def show_whatsapp(self, obj):
        return obj.whatsapp or "-"
    show_whatsapp.short_description = "WhatsApp"

    def show_instagram(self, obj):
        return obj.instagram or "-"
    show_instagram.short_description = "Instagram"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency', 'duration_days', 'moyka', 'unlimited_carwash')
    search_fields = ('name',)
    list_filter = ('duration_days', 'unlimited_carwash')
    ordering = ('price',)


# ----------------- UserSubscription -----------------
@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription', 'start_date', 'end_date', 'used_washes', 'is_active', 'has_washes_left')
    list_filter = ('start_date', 'end_date')
    search_fields = ('user__phone', 'subscription__name')
    readonly_fields = ('used_washes',)

    def is_active(self, obj):
        """Активна ли подписка (если end_date не истёк)"""
        from django.utils import timezone
        return obj.end_date >= timezone.now().date()
    is_active.boolean = True
    is_active.short_description = "Активна?"

    def has_washes_left(self, obj):
        return obj.has_washes_left()
    has_washes_left.boolean = True
    has_washes_left.short_description = "Остались мойки?"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car_wash', 'date', 'time','get_status', 'user_subscription')
    list_filter = ('date', 'car_wash')
    search_fields = ('user__phone', 'car_wash__name')
    readonly_fields = ('user_subscription',)
    ordering = ('-date', '-time')

    def get_status(self, obj):
        """Показ статуса, если есть"""
        return getattr(obj, 'status', '—')
    get_status.short_description = "Статус"

    def save_model(self, request, obj, form, change):
        """При подтверждении брони — списывает 1 мойку"""
        super().save_model(request, obj, form, change)
        if hasattr(obj, 'status') and obj.status == 'confirmed' and obj.user_subscription:
            if not change or 'status' in form.changed_data:
                obj.user_subscription.used_washes += 1
                obj.user_subscription.save()


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at')
    search_fields = ('user__phone', 'message')
    readonly_fields = ('created_at',)