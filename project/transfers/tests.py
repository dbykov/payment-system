import decimal

from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

import helpers
from accounts.enums import Currency
from transfers.models import Transfer


class TestTransfers(APITestCase):
    def setUp(self) -> None:
        self.user = helpers.create_user('alice', 'secret')
        http_auth_header = f'Token {self.user.auth_token.key}'
        self.client.credentials(HTTP_AUTHORIZATION=http_auth_header)

        self.other_user = helpers.create_user('bob', 'secret')

        helpers.set_exchange_rate(Currency.USD, decimal.Decimal(1.00))
        helpers.set_exchange_rate(Currency.CNY, decimal.Decimal(6.94))
        helpers.set_exchange_rate(Currency.EUR, decimal.Decimal(0.90))
        helpers.set_commission_fee(decimal.Decimal(2))

    def test_transfer_from_foreign_account(self):
        # setup:
        usd_acc = self.other_user.accounts.get(currency=Currency.USD.value)
        cny_acc = self.user.accounts.get(currency=Currency.CNY.value)
        amount = 10

        # when:
        response = self.client.post(reverse('transfer-create'), {
            'from_acc': usd_acc.id,
            'to_acc': cny_acc.id,
            'amount': amount
        })

        # then:
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_transfer_too_much(self):
        # setup:
        usd_acc = self.user.accounts.get(currency=Currency.USD.value)
        cny_acc = self.user.accounts.get(currency=Currency.CNY.value)
        amount = 1000

        # when:
        response = self.client.post(reverse('transfer-create'), {
            'from_acc': usd_acc.id,
            'to_acc': cny_acc.id,
            'amount': amount
        })

        # then:
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inner_transfer(self):
        # setup:
        usd_acc = self.user.accounts.get(currency=Currency.USD.value)
        cny_acc = self.user.accounts.get(currency=Currency.CNY.value)
        amount = 10

        # when:
        response = self.client.post(reverse('transfer-create'), {
            'from_acc': usd_acc.id,
            'to_acc': cny_acc.id,
            'amount': amount
        })

        # then:
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        usd_acc.refresh_from_db()
        cny_acc.refresh_from_db()
        self.assertEqual(usd_acc.balance, decimal.Decimal(90))
        self.assertEqual(cny_acc.balance,
                         helpers.round_decimal(decimal.Decimal(69.4)))

    def test_outer_transfer(self):
        # setup:
        usd_acc = self.user.accounts.get(currency=Currency.USD.value)
        cny_acc = self.other_user.accounts.get(currency=Currency.CNY.value)
        amount = 10

        # when:
        response = self.client.post(reverse('transfer-create'), {
            'from_acc': usd_acc.id,
            'to_acc': cny_acc.id,
            'amount': amount
        })

        # then:
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        usd_acc.refresh_from_db()
        cny_acc.refresh_from_db()
        self.assertEqual(usd_acc.balance, decimal.Decimal(90))
        self.assertEqual(cny_acc.balance,
                         helpers.round_decimal(decimal.Decimal(68.012)))

    def test_list(self):
        # setup:
        mixer.cycle(3).blend(
            Transfer,
            from_acc=(a for a in self.user.accounts.all()))

        # when:
        response = self.client.get(reverse('transfer-list'))

        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filtering(self):
        # setup:
        mixer.cycle(3).blend(
            Transfer,
            from_acc=(a for a in self.user.accounts.all()))

        # when:
        response = self.client.get(reverse('transfer-list'), {
            'from_acc__currency': Currency.USD.value,
        })

        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_ordering(self):
        # setup:
        mixer.cycle(3).blend(
            Transfer,
            sent_amount=(a for a in (2, 3, 1)),
            from_acc=(a for a in self.user.accounts.all()))

        # when:
        response = self.client.get(reverse('transfer-list'), {
            'ordering': "sent_amount",
        })

        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
