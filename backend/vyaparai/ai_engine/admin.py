from django.contrib import admin
from .models import AIChatSession, AIChatMessage, AIRecommendation


@admin.register(AIChatSession)
class AIChatSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'mentor_type', 'language', 'created_at', 'updated_at']
    list_filter = ['mentor_type', 'language', 'created_at']
    search_fields = ['user__email']


@admin.register(AIChatMessage)
class AIChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'sender', 'created_at']
    list_filter = ['sender', 'created_at']
    search_fields = ['message']


@admin.register(AIRecommendation)
class AIRecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'recommendation_type', 'is_used', 'created_at']
    list_filter = ['recommendation_type', 'is_used', 'created_at']
    search_fields = ['user__email']