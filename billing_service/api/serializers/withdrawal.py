from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import serializers
from common.services.daos import AccountDAO

User = get_user_model()


class WithdrawalSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, max_value=Decimal('-0.01'))

    def validate_amount(self, value: Decimal) -> Decimal:
        account = AccountDAO.get_account_by_user(self.context['user'])
        if account.balance < abs(value):
            raise serializers.ValidationError('Insufficient funds')

        return value
