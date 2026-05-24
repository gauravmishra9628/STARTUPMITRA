from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Subscription, PaymentTransaction
from .serializers import SubscriptionSerializer, PaymentTransactionSerializer
from django.shortcuts import get_object_or_404


class SubscriptionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        subs = Subscription.objects.filter(user=request.user)
        return Response(SubscriptionSerializer(subs, many=True).data)

    def post(self, request):
        # create or update subscription (stub)
        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentWebhookView(APIView):
    # In production this should be unauthenticated and verify provider signature
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        # minimal stub to record a transaction
        serializer = PaymentTransactionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'received'})
