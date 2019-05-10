import datetime

import boto3
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
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
        ad_data['user'] = request.user.id
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
        daily_views = ad.daily_views.filter(date=datetime.date.today()).first()
        if daily_views:
            daily_views.views += 1
            daily_views.save()
        else:
            daily_views = models.DailyAdViews(ad_id=ad.id, views=1,
                                              date=datetime.date.today())
        ad.save()
        daily_views.save()
        ad.views_today = daily_views.views
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


class ListAdsAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return self.search()

    def search(self):
        params = self.request.GET
        if 'city_id' in params:
            queryset = models.Ad.objects.filter(city_id=params['city_id'])
        elif 'city' in params:
            queryset = models.Ad.objects.filter(city__name=params['city'])
        elif 'region_id' in params:
            queryset = models.Ad.objects.filter(city__region_id=params['region_id'])
        elif 'region' in params:
            queryset = models.Ad.objects.filter(city__region__name=params['region'])
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'message': 'Region and city fields are missing.'
                })

        if 'model_id' in params:
            queryset = queryset.filter(model_id=params['model_id'])
        elif 'model' in params:
            queryset = queryset.filter(model__name=params['model'])
        elif 'make_id' in params:
            queryset = queryset.filter(model__make_id=params['make_id'])
        elif 'make' in params:
            queryset = queryset.filter(model__make__name=params['make'])
        queryset = queryset.filter(
            status=models.Ad.APPROVED, is_active=True, is_verified=True
        )

        if 'year_from' in params:
            queryset = queryset.filter(year__gte=params['year_from'])
        if 'year_to' in params:
            queryset = queryset.filter(year__lte=params['year_to'])

        if 'price_from' in params:
            queryset = queryset.filter(price__gte=params['price_from'])
        if 'price_to' in params:
            queryset = queryset.filter(price__lte=params['price_to'])

        if 'registration_city' in params:
            queryset = queryset.filter(registration_city_id=params['registration_city'])

        if 'color' in params:
            queryset = queryset.filter(color=params['color'])

        if 'mileage_from' in params:
            queryset = queryset.filter(mileage__gte=params['mileage_from'])
        if 'mileage_to' in params:
            queryset = queryset.filter(mileage__lte=params['mileage_to'])

        if 'transmission' in params:
            queryset = queryset.filter(transmission_type=params['transmission'])

        if 'assembly' in params:
            queryset = queryset.filter(assembly_type=params['assembly'])

        if self.request.user.is_authenticated:
            queryset = queryset.annotate(
                favorited=Count(
                    'favorited_ads',
                    filter=Q(favorited_ads__user_id=self.request.user.id)
                )
            )

        if 'sort_by' in params:
            queryset = self.sort_queryset_by(queryset, params['sort_by'])
        else:
            queryset = queryset.order_by('-created_at')

        queryset = queryset.select_related('model').prefetch_related('photos')
        paginator = Paginator(queryset, 10)
        if 'page' in params:
            try:
                results = paginator.get_page(params['page'])
            except:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        'message': 'Invalid page number.'
                    }
                )
        else:
            results = paginator.get_page(1)

        serializer = serializers.AdDetailsSerializer(results, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data={
                'items': serializer.data,
                'page': results.number,
                'total_pages': paginator.num_pages,
                'count': paginator.count
            }
        )

    def sort_queryset_by(self, queryset, sort_by):
        if sort_by == 'PRICE_LOW_TO_HIGH':
            return queryset.order_by('price')
        elif sort_by == 'PRICE_HIGH_TO_LOW':
            return queryset.order_by('-price')
        elif sort_by == 'DATE_RECENT_FIRST':
            return queryset.order_by('-created_at')
        elif sort_by == 'DATE_OLDEST_FIRST':
            return queryset.order_by('created_at')
        elif sort_by == 'YEAR_LATEST_FIRST':
            return queryset.order_by('-year')
        elif sort_by == 'YEAR_OLDEST_FIRST':
            return queryset.order_by('year')
        elif sort_by == 'MILEAGE_LOW_TO_HIGH':
            return queryset.order_by('mileage')
        elif sort_by == 'MILEAGE_HIGH_TO_LOW':
            return queryset.order_by('-mileage')
        pass


class FavoritedAdsAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        try:
            models.FavoritedAd.objects.get_or_create(
                 ad_id=id, user_id=request.user.id
             )
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'message': 'Ad does not exist'
                }
             )


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
