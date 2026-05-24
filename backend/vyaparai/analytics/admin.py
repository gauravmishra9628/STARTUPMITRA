from django.contrib import admin
from .models import RevenueReport, Event


@admin.register(RevenueReport)
class RevenueReportAdmin(admin.ModelAdmin):
    list_display = ('period_start', 'period_end', 'total_revenue', 'created_at')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'user', 'created_at')
