from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class PurchaseSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal('0.01'))
