from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers

from accounts.models import Account
from transfers.models import Transfer


class TransferSerializer(serializers.Serializer):
    current_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=True)
    from_acc = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        required=True)
    to_acc = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        required=True)
    amount = serializers.DecimalField(
        min_value=0,
        max_digits=24,
        decimal_places=4)

    def validate(self, attrs):
        if attrs['current_user'] != attrs['from_acc'].user:
            raise ValidationError({'from_acc': 'Счет не найден'})
        return super().validate(attrs)


class TransferListSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(source='from_acc.currency')
    username = serializers.CharField(source='to_acc.user.username')

    class Meta:
        model = Transfer
        fields = ('currency', 'sent_amount', 'username',
                  'commission_fee', 'created_at')
