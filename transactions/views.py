from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from transactions import serializers, models


class PaymentViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PaymentSerializer
    queryset = models.Payment.objects.all()
