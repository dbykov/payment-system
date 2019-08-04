import decimal

from django.core.management.base import BaseCommand

import helpers
from accounts.enums import Currency


class Command(BaseCommand):
    help = 'Установка размера комиссии'

    def add_arguments(self, parser):
        parser.add_argument('fee', nargs='?', type=str)

    def handle(self, *args, **options):
        fee = decimal.Decimal(options['fee'])

        helpers.set_commission_fee(fee)

        self.stdout.write(
            self.style.SUCCESS(f'Размер комиссии: {fee}'))
