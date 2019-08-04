from django.db import models

import mixins


class Transfer(mixins.DateMixin, models.Model):
    from_acc = models.ForeignKey(
        'accounts.Account',
        on_delete=models.PROTECT,
        related_name='sent_transfers')
    to_acc = models.ForeignKey(
        'accounts.Account',
        on_delete=models.PROTECT,
        related_name='received_transfers')
    sent_amount = models.DecimalField(
        verbose_name='Объем трансфера',
        max_digits=24,
        decimal_places=4)
    received_amount = models.DecimalField(
        verbose_name='Объем трансфера',
        max_digits=24,
        decimal_places=4)
    commission_fee = models.DecimalField(
        verbose_name='Размер комиссии',
        max_digits=24,
        decimal_places=4)

    class Meta:
        verbose_name = 'Переводы'
