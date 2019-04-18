from rest_framework import serializers

from common.serializers import CitySerializer
from listings import models
from vehicles.serializers import FeatureSerializer


class AdSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True)

    class Meta:
        model = models.Ad
        fields = ('id', 'user', 'model', 'variant', 'year', 'color', 'mileage',
                  'body_type', 'transmission_type', 'modification_type',
                  'gas_equipment', 'assembly_type', 'fuel_type', 'address',
                  'city', 'registration_city', 'price', 'contact', 'contact_person',
                  'comments', 'features', 'views', 'youtube_link', 'is_active',
                  'is_verified', 'is_featured', 'status')


class AdDetailsSerializer(serializers.ModelSerializer):

    features = FeatureSerializer(many=True)
    city = CitySerializer()
    registration_city = CitySerializer()
    model = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    body_type = serializers.SerializerMethodField()
    transmission_type = serializers.SerializerMethodField()
    modification_type = serializers.SerializerMethodField()
    fuel_type = serializers.SerializerMethodField()
    assembly_type = serializers.SerializerMethodField()

    class Meta:
        model = models.Ad
        fields = ('id', 'user', 'model', 'variant', 'year', 'color', 'mileage',
                  'body_type', 'transmission_type', 'modification_type',
                  'gas_equipment', 'assembly_type', 'fuel_type', 'address',
                  'city', 'registration_city', 'price', 'contact', 'contact_person',
                  'comments', 'features', 'views', 'youtube_link', 'updated_at',
                  'photos', 'assembly_type')

    def get_model(self, obj):
        return '{0} {1} {2}'.format(obj.model.make.name, obj.model.name, obj.year)

    def get_photos(self, obj):
        photos = []
        for p in obj.photos.all():
            photos.append(p.uuid)
        return photos

    def get_body_type(self, obj):
        return obj.get_body_type_display()

    def get_transmission_type(self, obj):
        return obj.get_transmission_type_display()

    def get_modification_type(self, obj):
        return obj.get_modification_type_display()

    def get_fuel_type(self, obj):
        return obj.get_fuel_type_display()

    def get_assembly_type(self, obj):
        return obj.get_assembly_type_display()

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



