from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from vehicles import serializers, models


class MakeViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.MakeSerializer
    queryset = models.Make.objects.all()


class ModelViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.ModelSerializer
    queryset = models.Model.objects.all()


class VariantViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.VariantSerializer
    queryset = models.Variant.objects.all()


class FeatureViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.FeatureSerializer
    queryset = models.Feature.objects.all()
