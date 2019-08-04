from django.db import models
from django.db.models import CheckConstraint, Q

import mixins
from accounts.enums import Currency


class Account(mixins.DateMixin, models.Model):
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='accounts')
    currency = models.TextField(
        verbose_name='Валюта',
        choices=Currency.to_choices())
    balance = models.DecimalField(
        verbose_name='Текущий баланс',
        default=0,
        max_digits=24,
        decimal_places=4)

    class Meta:
        verbose_name = 'Счет'
        unique_together = ('user', 'currency')
        constraints = [
            CheckConstraint(
                check=Q(balance__gte=0),
                name='positive_balance')
        ]
