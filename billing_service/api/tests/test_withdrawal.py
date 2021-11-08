from datetime import datetime

from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from rest_framework import status
from oauth2_provider.models import AccessToken

import common.constants
from common.models import UserAccount, AccountOperation

from .base_api_test import BaseApiTestCase

User = get_user_model()


class WithdrawalTestCase(BaseApiTestCase):
    url = reverse('withdrawal')
    required_scope = 'withdrawal'

    def setUp(self) -> None:
        super(WithdrawalTestCase, self).setUp()
        self.user_account.balance += 1000
        self.user_account.save()

    def test_withdrawal_with_valid_data(self):
        data = {
            'amount': '-10.00'
        }
        self.assertEqual(UserAccount.objects.get(pk=self.user_account.pk).balance, 1000)

        response = self.client.post(
            path=self.url, data=data, format='json',
            HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserAccount.objects.get(pk=self.user_account.pk).balance, 990)
        self.assertEqual(AccountOperation.objects.count(), 1)
        operation = AccountOperation.objects.first()
        self.assertEqual(operation.operation_type, common.constants.WITHDRAWAL_OPERATION)
        self.assertEqual(operation.amount, -10)

    def test_withdrawal_with_positive_amount(self):
        data = {
            'amount': '10.00'
        }
        response = self.client.post(
            path=self.url, data=data, format='json',
            HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserAccount.objects.get(pk=self.user_account.pk).balance, 1000)

    def test_withdrawal_with_invalid_decimal(self):
        data = {
            'amount': '10.12345'
        }
        response = self.client.post(
            path=self.url, data=data, format='json',
            HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserAccount.objects.get(pk=self.user_account.pk).balance, 1000)

    def test_withdrawal_without_token(self):
        data = {
            'amount': '10.00'
        }
        response = self.client.post(
            path=self.url, data=data, format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(UserAccount.objects.get(pk=self.user_account.pk).balance, 1000)

    def test_withdrawal_with_token_with_invalid_scope(self):
        acc_access_token = AccessToken.objects.create(
            token='new_token',
            scope='account',
            user=self.user,
            expires=datetime.max
        )
        data = {
            'amount': '10.00'
        }
        response = self.client.post(
            path=self.url,
            data=data,
            format='json',
            HTTP_AUTHORIZATION='Bearer {}'.format(acc_access_token.token)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(UserAccount.objects.get(pk=self.user_account.pk).balance, 1000)
