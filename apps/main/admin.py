from django.contrib import admin
<<<<<<< HEAD:api/admin.py
from .models import Onboarding, FAQ, SupportMessage, Marka, Model, Body
=======
from .models import *
>>>>>>> f1e4b04 (apps):apps/main/admin.py
from django.utils.safestring import mark_safe

class ImagePreviewMixin:
    @admin.display(description='Изображение')
    def image_preview(self, obj):
        if hasattr(obj, 'image') and obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height:100px; max-width:100px;" />')
        return 'Нет изображения'

@admin.register(Onboarding)
class OnboardingAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ('title', 'image_preview',)
    search_fields = ('title',)


@admin.register(Marka)
class MarkaAdmin(admin.ModelAdmin):
    list_display = ('marka',)
    search_fields = ('marka',)

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('model', 'marka')
    list_filter = ('marka',)
    search_fields = ('model', 'marka__marka')

@admin.register(Body)
class BodyAdmin(admin.ModelAdmin):
    list_display = ('kuzov',)
    search_fields = ('kuzov',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question',)
    search_fields = ('question',)


@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'created_at',)
    search_fields = ('subject', 'user__email',)
    readonly_fields = ('subject', 'user', 'message', 'created_at',)


@admin.register(Marka)
class MarkaAdmin(admin.ModelAdmin):
    list_display = ('marka',)
    search_fields = ('marka',)

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('model', 'marka')
    list_filter = ('marka',)
    search_fields = ('model', 'marka__marka')

@admin.register(Body)
class BodyAdmin(admin.ModelAdmin):
    list_display = ('kuzov',)
    search_fields = ('kuzov',)

@admin.register(MycarProfile)
class MycarProfileAdmin(admin.ModelAdmin):
    icon_name = "directions_car"
    list_display = ('user', 'marka', 'model', 'gos_number')
    search_fields = ('user', 'marka', 'model', 'gos_number')