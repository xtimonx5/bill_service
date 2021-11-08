from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.transaction import atomic

from common.models import UserAccount, AccountOperation
from common.services.daos import AccountDAO

import common.constants

User = get_user_model()


class BaseBalanceChangeUseCase:
    OPERATION_TYPE = None

    def __init__(self, user: User, amount: Decimal) -> None:
        self._user = user
        self._amount = amount

    @atomic
    def execute(self) -> UserAccount:
        account = AccountDAO.change_balance(self._user, self._amount)
        AccountOperation.objects.create(
            account=account,
            operation_type=self.OPERATION_TYPE,
            amount=self._amount
        )
        return account
