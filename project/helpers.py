import decimal

import typeguard
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import transaction
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from accounts.enums import Currency
from accounts.models import Account

__all__ = ('create_user', )


@typeguard.typechecked
def create_user(username: str, password: str) -> User:
    user = User.objects.create_user(username, None, password)

    Token.objects.get_or_create(user=user)

    Account.objects.get_or_create(
        currency=Currency.USD.value, user=user, balance=100)
    Account.objects.get_or_create(
        currency=Currency.CNY.value, user=user)
    Account.objects.get_or_create(
        currency=Currency.EUR.value, user=user)

    return user


@typeguard.typechecked
def set_exchange_rate(currency: Currency, rate: decimal.Decimal = 1):
    cache.set(currency.value, rate, None)


@typeguard.typechecked
def set_commission_fee(percents: decimal.Decimal = 1):
    cache.set('fee', percents, None)


@typeguard.typechecked
def get_commission_fee() -> decimal.Decimal:
    return cache.get('fee')


@typeguard.typechecked
def convert_currency(from_currency: Currency, to_currency: Currency,
                     amount: decimal.Decimal) -> decimal.Decimal:
    from_rate = cache.get(from_currency.value)
    if not from_rate:
        raise ValidationError(
            f"Не установлен курс валюты {from_currency.value}")
    to_rate = cache.get(to_currency.value)

    if not to_rate:
        raise ValidationError(
            f"Не установлен курс валюты {to_currency.value}")

    return round_decimal(to_rate * amount / from_rate)


@typeguard.typechecked
def round_decimal(amount: decimal.Decimal) -> decimal.Decimal:
    return decimal.Decimal(amount).quantize(decimal.Decimal('.0001'))


@typeguard.typechecked
def take_commission_fee(amount: decimal.Decimal) -> decimal.Decimal:
    commision_fee = get_commission_fee()
    if not commision_fee:
        raise ValidationError(
            f"Не установлен размер комиссии")

    return amount - round_decimal(amount * commision_fee / 100)
