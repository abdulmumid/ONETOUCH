from django.contrib import admin
from .models import Marka, Model, Body

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