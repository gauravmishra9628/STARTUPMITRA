from django.db import models
from django.conf import settings


class Category(models.Model):
    """Business category model"""
    name = models.CharField(max_length=100)
    name_hi = models.CharField(max_length=100, blank=True)
    icon = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    description_hi = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class BusinessIdea(models.Model):
    """Business idea model"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    title = models.CharField(max_length=200)
    title_hi = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    description_hi = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='businesses')
    min_investment = models.DecimalField(max_digits=12, decimal_places=2)
    max_investment = models.DecimalField(max_digits=12, decimal_places=2)
    estimated_profit = models.DecimalField(max_digits=10, decimal_places=2)
    profit_percentage = models.IntegerField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    skills_required = models.JSONField(default=list)
    market_demand = models.IntegerField(default=50)
    risk_level = models.IntegerField(default=50)
    is_featured = models.BooleanField(default=False)
    is_ai_generated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'business_ideas'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class SavedBusiness(models.Model):
    """User saved business ideas"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_businesses')
    business = models.ForeignKey(BusinessIdea, on_delete=models.CASCADE, related_name='saved_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'saved_businesses'
        unique_together = ['user', 'business']


class BusinessRoadmap(models.Model):
    """AI-generated business roadmaps"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='business_roadmaps')
    business = models.ForeignKey(BusinessIdea, on_delete=models.CASCADE, related_name='roadmaps')
    roadmap_data = models.JSONField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'business_roadmaps'
        ordering = ['-created_at']