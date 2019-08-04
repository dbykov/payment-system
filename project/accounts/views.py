from rest_framework.response import Response
from rest_framework.views import APIView


class AccountsList(APIView):
    def get(self, request):
        accounts = request.user.accounts.values('id', 'currency', 'balance')
        return Response(accounts)
