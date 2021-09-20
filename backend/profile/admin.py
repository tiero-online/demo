from django.contrib import admin
from backend.profile.models import UserProfile


# class ProfileAdmin(admin.ModelAdmin):


admin.site.register(UserProfile)
