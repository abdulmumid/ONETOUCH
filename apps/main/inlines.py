from django.contrib import admin
from .models import MycarProfile

class MycarProfileInline(admin.StackedInline):
    model = MycarProfile
    extra = 0