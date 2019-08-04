from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

import helpers
from accounts.enums import Currency


class TestAccounts(APITestCase):
    def setUp(self) -> None:
        self.user = helpers.create_user('john', 'secret')
        http_auth_header = f'Token {self.user.auth_token.key}'
        self.client.credentials(HTTP_AUTHORIZATION=http_auth_header)

    def test_show_accounts_info(self):
        # when:
        response = self.client.get(reverse('accounts-list'))

        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [
            {'id': 1, 'currency': Currency.USD.value, 'balance': 100},
            {'id': 2, 'currency': Currency.CNY.value, 'balance': 0},
            {'id': 3, 'currency': Currency.EUR.value, 'balance': 0},
        ])
