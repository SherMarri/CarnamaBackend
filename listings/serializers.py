from rest_framework import serializers

from listings import models
from vehicles.serializers import FeatureSerializer


class AdSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True)

    class Meta:
        model = models.Ad
        fields = ('id', 'user', 'model', 'variant', 'year', 'color', 'mileage', 'address',
                  'city', 'price', 'contact', 'description', 'features', 'views',
                  'is_active', 'is_verified', 'is_featured')
