from django.db import models
from django.conf import settings
from businesses.models import BusinessIdea


class Roadmap(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_roadmaps')
    title = models.CharField(max_length=255)
    business = models.ForeignKey(BusinessIdea, on_delete=models.SET_NULL, null=True, blank=True)
    roadmap_data = models.JSONField()
    language = models.CharField(max_length=10, default='en')
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'roadmaps'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.user}"
