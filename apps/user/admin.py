from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTP, Avatar
from .inlines import  AvatarInline, UserSubscriptionInline
from apps.main.inlines import MycarProfileInline

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    icon_name = "person"
    model = CustomUser
    list_display = ('id', 'email', 'first_name', 'phone', 'is_staff', 'is_verified', 'is_active')
    list_filter = ('is_staff', 'is_verified', 'is_active')
    search_fields = ('email', 'first_name', 'phone')
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'sur_name', 'phone')}),
        ('Права', {'fields': ('is_staff', 'is_active', 'is_verified', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важное', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'phone', 'password1', 'password2', 'is_staff', 'is_verified')}
        ),
    )
    inlines = [MycarProfileInline, AvatarInline, UserSubscriptionInline]

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    icon_name = "vpn_key"
    list_display = ('user', 'code', 'purpose', 'is_used', 'created_at', 'expires_at_display')
    list_filter = ('purpose', 'is_used', 'created_at')
    search_fields = ('user__email', 'code')
    readonly_fields = ('created_at',)

    @admin.display(description="Истекает")
    def expires_at_display(self, obj):
        return obj.expires_at



@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    icon_name = "face"
    list_display = ('user', 'image')