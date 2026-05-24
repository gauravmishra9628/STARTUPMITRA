from django.urls import path
from .views import SubscriptionView, PaymentWebhookView

urlpatterns = [
    path('subscriptions/', SubscriptionView.as_view(), name='subscriptions'),
    path('webhook/', PaymentWebhookView.as_view(), name='payment-webhook'),
]
