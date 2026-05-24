from django.contrib import admin
from .models import Subscription, PaymentTransaction


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'active', 'started_at', 'expires_at')


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'provider', 'created_at')
