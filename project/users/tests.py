from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from accounts.enums import Currency
from accounts.models import Account


class TestUsers(APITestCase):
    def test_user_register(self):
        # when:
        response = self.client.post(reverse('users-register'), {
            'username': 'john', 'password': 'secret'
        })
        # then:
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Account.objects.get(currency=Currency.USD.value).balance,
            100)

    def test_user_obtain_token(self):
        # setup:
        User.objects.create_user('john', None, 'secret')

        # when:
        response = self.client.post(reverse('users-obtain-token'), {
            'username': 'john', 'password': 'secret'
        })
        # then:
        self.assertTrue('token' in response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
