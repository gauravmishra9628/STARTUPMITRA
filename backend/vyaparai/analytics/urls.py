from django.urls import path
from .views import AnalyticsOverview, RevenueReportView

urlpatterns = [
    path('overview/', AnalyticsOverview.as_view(), name='analytics-overview'),
    path('revenue/', RevenueReportView.as_view(), name='analytics-revenue'),
]
