from rest_framework import serializers

from listings import models
from vehicles.serializers import FeatureSerializer


class AdSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True)

    class Meta:
        model = models.Ad
        fields = ('id', 'user', 'model', 'variant', 'year', 'color', 'mileage', 'address',
                  'city', 'price', 'contact', 'comments', 'features', 'views', 'youtube_link',
                  'is_active', 'is_verified', 'is_featured', 'status')


class AutosaleRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AutosaleRequest
        fields = ('id', 'user', 'model', 'year', 'color', 'name', 'contact',
                  'status')


class DailyAdViewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DailyAdViews
        fields = ('id', 'ad', 'views', 'created_at')


class SavedSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SavedSearch
        fields = ('id', 'user', 'make', 'model', 'variant')


class CallbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Callback
        fields = ('id', 'ad', 'user', 'contact', 'status')


class ReportedAdSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ReportedAd
        fields = ('id', 'user', 'ad', 'comment', 'reason', 'total_reports',
                  'is_banned')



