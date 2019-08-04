from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from transfers.models import Transfer
from transfers.serializers import TransferSerializer, TransferListSerializer
from . import utils


class TransfersCreate(APIView):
    def post(self, request):
        serializer = TransferSerializer(data={
            'current_user': request.user.id,
            **request.data.dict()})

        serializer.is_valid(raise_exception=True)
        transfer = utils.make_transfer(serializer.validated_data)

        return Response({
            'from_acc': transfer.from_acc.id,
            'to_acc': transfer.to_acc.id,
            'sent_amount': transfer.sent_amount,
            'received_amount': transfer.received_amount,
        }, status.HTTP_201_CREATED)


class TransfersList(generics.CreateAPIView, generics.ListAPIView):
    queryset = Transfer.objects.select_related(
        'to_acc__user', 'from_acc__user').all()
    serializer_class = TransferListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['from_acc__currency', 'to_acc__user__username']
    ordering_fields = ['sent_amount', 'commission_fee', 'created_at']

    def get_queryset(self):
        return super().get_queryset().filter(from_acc__user=self.request.user)

