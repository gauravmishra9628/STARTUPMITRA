from django.contrib import admin
from .models import User, UserSession


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_premium', 'language', 'created_at']
    list_filter = ['is_premium', 'language', 'created_at']
    search_fields = ['email', 'username', 'first_name', 'last_name']


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_id', 'created_at', 'last_activity']
    list_filter = ['created_at']
    search_fields = ['user__email', 'session_id']