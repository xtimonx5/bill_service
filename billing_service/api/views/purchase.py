from django.conf import settings

from rest_framework import views
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.contrib.rest_framework import TokenHasScope

from common.services.usecases import PurchaseUseCase

from api.serializers import PurchaseSerializer


class PurchaseView(views.APIView):
    permission_classes = [TokenHasScope, ]

    required_scopes = [settings.PURCHASE_SCOPE, ]

    def _perform_purchase(self, data: dict) -> None:
        PurchaseUseCase(user=self.request.user, amount=data['amount']).execute()

    def post(self, request: Request) -> Response:
        serializer = PurchaseSerializer(data=request.data)
        if serializer.is_valid():
            self._perform_purchase(serializer.validated_data)
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
