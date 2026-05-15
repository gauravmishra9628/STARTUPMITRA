from django.contrib import admin
from .models import Category, BusinessIdea, SavedBusiness, BusinessRoadmap


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_hi', 'icon', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'name_hi']


@admin.register(BusinessIdea)
class BusinessIdeaAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'min_investment', 'max_investment', 'difficulty', 'is_featured', 'is_ai_generated']
    list_filter = ['category', 'difficulty', 'is_featured', 'is_ai_generated']
    search_fields = ['title', 'title_hi', 'description']
    list_editable = ['is_featured']


@admin.register(SavedBusiness)
class SavedBusinessAdmin(admin.ModelAdmin):
    list_display = ['user', 'business', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'business__title']


@admin.register(BusinessRoadmap)
class BusinessRoadmapAdmin(admin.ModelAdmin):
    list_display = ['user', 'business', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'created_at']
    search_fields = ['user__email', 'business__title']