from rest_framework import serializers

from vehicles import models


class MakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Make
        fields = ('id', 'name', 'vehicle_type', 'region', 'is_popular')


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model
        fields = ('id', 'name', 'make')


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Variant
        fields = ('id', 'name', 'model')


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Feature
        fields = ('id', 'name', 'code', 'description', 'vehicle_type')
