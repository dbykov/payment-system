import decimal

from django.core.management.base import BaseCommand

import helpers
from accounts.enums import Currency


class Command(BaseCommand):
    help = 'Установка курса валют'

    def add_arguments(self, parser):
        parser.add_argument('currency', nargs='?', type=str)
        parser.add_argument('rate', nargs='?', type=str)

    def handle(self, *args, **options):
        currency = Currency.from_str(options['currency'])
        rate = decimal.Decimal(options['rate'])

        helpers.set_exchange_rate(currency, rate)

        self.stdout.write(
            self.style.SUCCESS(f'Курс устновлен: {currency.value} = {rate}'))
