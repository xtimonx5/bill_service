from django.contrib.auth import get_user_model

import common.constants
from .base_account_balance_changer import BaseBalanceChangeUseCase

User = get_user_model()


class WithdrawalUseCase(BaseBalanceChangeUseCase):
    OPERATION_TYPE = common.constants.WITHDRAWAL_OPERATION
