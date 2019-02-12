from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from listings import serializers, models
from vehicles.models import Feature


class PostAdAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def associate_ad_features(self, ad, feature_ids):
        """
        Associates selected features of a vehicle to an ad
        :param ad: Ad to associate with
        :param feature_ids: List of feature ids to associate with given ad
        :return:
        """
        features = Feature.objects.filter(id__in=feature_ids)
        ad.features.set(features)

    def post(self, request):
        data = request.data
        ad_data = data['ad']
        ad_feature_ids = data['feature_ids']
        serializer = serializers.AdSerializer(data=ad_data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        ad = serializer.save()
        self.associate_ad_features(ad, ad_feature_ids)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class AutosaleRequestViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = serializers.AutosaleRequestSerializer
    queryset = models.AutosaleRequest.objects.all()


class DailyAdViewsViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.DailyAdViewsSerializer
    queryset = models.DailyAdViews.objects.all()


class SavedSearchViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.SavedSearchSerializer
    queryset = models.SavedSearch.objects.all()


class CallbackViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CallbackSerializer
    queryset = models.Callback.objects.all()


class ReportedAdViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ReportedAdSerializer
    queryset = models.ReportedAd.objects.all()
