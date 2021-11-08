from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.transaction import atomic

from common.models import UserAccount, AccountOperation
from common.services.daos import AccountDAO

import common.constants
from .base_account_balance_changer import BaseBalanceChangeUseCase

User = get_user_model()


class WithdrawalUseCase(BaseBalanceChangeUseCase):
    OPERATION_TYPE = common.constants.WITHDRAWAL_OPERATION
