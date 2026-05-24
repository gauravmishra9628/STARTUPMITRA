from django.contrib import admin
from .models import Roadmap


@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_public', 'created_at')
    search_fields = ('title', 'user__email')
