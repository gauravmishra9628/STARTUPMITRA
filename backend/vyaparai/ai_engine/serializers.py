from rest_framework import serializers
from .models import AIChatSession, AIChatMessage, AIRecommendation


class AIChatSessionSerializer(serializers.ModelSerializer):
    """Serializer for AI Chat Session"""
    class Meta:
        model = AIChatSession
        fields = ['id', 'mentor_type', 'language', 'created_at', 'updated_at']


class AIChatMessageSerializer(serializers.ModelSerializer):
    """Serializer for AI Chat Message"""
    class Meta:
        model = AIChatMessage
        fields = ['id', 'sender', 'message', 'created_at']


class AIRecommendationSerializer(serializers.ModelSerializer):
    """Serializer for AI Recommendations"""
    class Meta:
        model = AIRecommendation
        fields = ['id', 'recommendation_type', 'recommendation_data', 'is_used', 'created_at']