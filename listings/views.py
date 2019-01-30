from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from listings import serializers
from listings.models import AdFeature


class PostAdAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def associate_ad_features(self, ad, feature_ids):
        """
        Associates selected features of a vehicle to an ad
        :param ad: Ad to associate with
        :param feature_ids: List of feature ids to associate with given ad
        :return:
        """
        ad_id = ad.id
        features = []
        for f in feature_ids:
            features.append(AdFeature(ad_id=ad_id, feature_id=f))
        AdFeature.objects.bulk_create(features)

    def post(self, request):
        data = request.data
        ad_data = data['ad']
        ad_features = data['features']
        serializer = serializers.AdSerializer(data=ad_data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors_)
        ad = serializer.save()
        self.associate_ad_features(ad, ad_features)
        return Response(status=status.HTTP_201_CREATED,
                        data={
                            'ad': serializer.data,
                            'features': []  # TODO: Plan how to return features in response
                        })
