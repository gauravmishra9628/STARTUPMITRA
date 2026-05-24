from rest_framework import serializers
from .models import Roadmap


class RoadmapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roadmap
        fields = '__all__'
        read_only_fields = ('user', 'created_at')
