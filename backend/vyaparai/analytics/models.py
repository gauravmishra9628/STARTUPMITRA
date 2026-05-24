from django.db import models
from django.conf import settings


class RevenueReport(models.Model):
    """Simple revenue tracking model"""
    period_start = models.DateField()
    period_end = models.DateField()
    total_revenue = models.DecimalField(max_digits=14, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'analytics_revenue_reports'

    def __str__(self):
        return f"Revenue {self.period_start} - {self.period_end}: {self.total_revenue}"


class Event(models.Model):
    """Generic analytics event for simple tracking"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    event_type = models.CharField(max_length=100)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'analytics_events'

    def __str__(self):
        return f"{self.event_type} @ {self.created_at}"
