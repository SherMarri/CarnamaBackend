from rest_framework import serializers

from common import models


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.City
        fields = ('id', 'name')
