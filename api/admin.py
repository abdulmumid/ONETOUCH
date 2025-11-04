from django.contrib import admin
from .models import Onboarding
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
