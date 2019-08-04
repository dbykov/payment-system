import decimal

import typeguard
from django.db import transaction
from django.db.models import F
from rest_framework.exceptions import ValidationError

import helpers
from accounts.enums import Currency
from accounts.models import Account
from transfers.models import Transfer


@typeguard.typechecked
def make_transfer(data: dict) -> Transfer:
    from_acc: Account = data['from_acc']
    from_currency: Currency = Currency.from_str(from_acc.currency)
    to_acc: Account = data['to_acc']
    to_currency: Currency = Currency.from_str(to_acc.currency)
    amount: decimal.Decimal() = data['amount']

    if from_acc.balance < amount:
        raise ValidationError("Недостаточно средств на счете")

    received_amount = helpers.convert_currency(
        from_currency, to_currency, amount)

    commission_fee = 0
    if from_acc.user != to_acc.user:
        commission_fee = helpers.get_commission_fee()
        received_amount = helpers.take_commission_fee(received_amount)

    with transaction.atomic():
        transfer = Transfer.objects.create(
            from_acc=from_acc,
            to_acc=to_acc,
            sent_amount=amount,
            received_amount=received_amount,
            commission_fee=commission_fee)

        Account.objects.filter(pk=from_acc.id).update(
            balance=F('balance') - transfer.sent_amount)
        Account.objects.filter(pk=to_acc.id).update(
            balance=F('balance') + transfer.received_amount)

    return transfer
