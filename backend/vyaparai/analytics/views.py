from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Event, RevenueReport
from .serializers import EventSerializer, RevenueReportSerializer
from django.contrib.auth import get_user_model
from businesses.models import BusinessIdea


class AnalyticsOverview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        User = get_user_model()
        user_count = User.objects.count()
        business_count = BusinessIdea.objects.count()
        recent_events = Event.objects.order_by('-created_at')[:10]
        events = EventSerializer(recent_events, many=True).data

        return Response({
            'user_count': user_count,
            'business_count': business_count,
            'recent_events': events,
        })


class RevenueReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        reports = RevenueReport.objects.order_by('-period_start')[:10]
        return Response(RevenueReportSerializer(reports, many=True).data)
