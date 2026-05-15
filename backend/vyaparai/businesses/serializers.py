from rest_framework import serializers
from .models import Category, BusinessIdea, SavedBusiness, BusinessRoadmap


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'name_hi', 'icon', 'description', 'description_hi']


class BusinessIdeaSerializer(serializers.ModelSerializer):
    """Serializer for BusinessIdea model"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_name_hi = serializers.CharField(source='category.name_hi', read_only=True)
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = BusinessIdea
        fields = [
            'id', 'title', 'title_hi', 'description', 'description_hi',
            'category', 'category_name', 'category_name_hi',
            'min_investment', 'max_investment', 'estimated_profit',
            'profit_percentage', 'difficulty', 'skills_required',
            'market_demand', 'risk_level', 'is_featured', 'is_ai_generated',
            'is_saved', 'created_at'
        ]

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavedBusiness.objects.filter(user=request.user, business=obj).exists()
        return False


class BusinessIdeaListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing business ideas"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = BusinessIdea
        fields = [
            'id', 'title', 'title_hi', 'category_name', 'min_investment',
            'max_investment', 'estimated_profit', 'profit_percentage',
            'difficulty', 'market_demand', 'risk_level', 'is_featured', 'is_saved'
        ]

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavedBusiness.objects.filter(user=request.user, business=obj).exists()
        return False


class SavedBusinessSerializer(serializers.ModelSerializer):
    """Serializer for SavedBusiness model"""
    business = BusinessIdeaListSerializer(read_only=True)

    class Meta:
        model = SavedBusiness
        fields = ['id', 'business', 'created_at']


class BusinessRoadmapSerializer(serializers.ModelSerializer):
    """Serializer for BusinessRoadmap model"""
    business_title = serializers.CharField(source='business.title', read_only=True)

    class Meta:
        model = BusinessRoadmap
        fields = ['id', 'business', 'business_title', 'roadmap_data', 'is_completed', 'created_at']