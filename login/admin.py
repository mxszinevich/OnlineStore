from django.contrib import admin

from login.models import UserProfile


@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    pass
