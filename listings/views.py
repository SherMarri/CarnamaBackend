import boto3
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from listings import serializers, models
from vehicles.models import Feature


class PostAdAPIView(APIView):
    permission_classes = (AllowAny,)

    def associate_ad_features(self, ad, feature_ids):
        """
        Associates selected features of a vehicle to an ad
        :param ad: Ad to associate with
        :param feature_ids: List of feature ids to associate with given ad
        :return:
        """
        features = Feature.objects.filter(id__in=feature_ids)
        ad.features.set(features)


    def associate_ad_photos(self, ad, image_ids):
        """
        Associates the images uploaded on S3 with this ad
        :param ad:
        :param image_ids:
        :return:
        """
        ad_photos = []
        for id in image_ids:
            ad_photos.append(models.AdPhoto(ad_id=ad.id, uuid=id))

        models.AdPhoto.objects.bulk_create(ad_photos)

    def post(self, request):
        data = request.data
        ad_data = data['ad']
        ad_feature_ids = data['feature_ids']
        ad_image_ids = data['image_ids']
        serializer = serializers.AdSerializer(data=ad_data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        ad = serializer.save()
        self.associate_ad_features(ad, ad_feature_ids)
        self.associate_ad_photos(ad, ad_image_ids)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class FetchAdAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, id):
        ad = models.Ad.objects.filter(
            id=id).select_related('model__make', 'city').prefetch_related(
            'photos', 'features').first()

        # Increment ad view
        ad.views += 1
        ad.save()
        if ad is None:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={
                                'message': 'Ad not found.'
                            })
        serializer = serializers.AdDetailsSerializer(ad)
        data = {
            'ad': serializer.data
        }
        return Response(status=status.HTTP_200_OK, data=data)



class GetPresignedUrlsAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        if 'files' not in data:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'Files missing'})

        urls = self.get_presigned_urls(data['files'])
        return Response(status=status.HTTP_200_OK, data=urls)

    def get_presigned_urls(self, files):
        urls = []
        s3 = boto3.client('s3')
        for f in files:
            response = s3.generate_presigned_url(
                'put_object', Params={'Bucket': 'carnama-assets', 'Key': f['id'],
                                      'ContentType': f['type']},
                ExpiresIn=120, HttpMethod='PUT')
            urls.append(response)
        return urls


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
