from rest_framework import serializers

from transactions import models


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Payment
        fields = ('id', 'order_id', 'ad', 'amount', 'package')
