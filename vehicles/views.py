from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from vehicles import serializers, models


class FetchMakesAPIView(ListAPIView):
    """
    API returns makes according to the search term and region
    POPULAR BRANDS and ALL MAKES
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        region = request.GET.get('region', None)
        search_term = ''
        if request.GET.get('term', None):
            search_term = request.GET.get('term')

        queryset = models.Make.objects.filter(
            region__name=region, name__istartswith=search_term
        ).order_by('name')
        serializer = serializers.MakeSerializer(queryset, many=True)
        popular_makes = queryset.filter(is_popular=True)
        if popular_makes.count() >= 7:
            popular_makes = popular_makes.all()[:7]
        else:
            popular_makes = popular_makes.all()
        popular_makes_serializer = serializers.MakeSerializer(popular_makes, many=True)
        return Response(status=status.HTTP_200_OK, data={
            'items': serializer.data,
            'popular': popular_makes_serializer.data
        })


class FetchModelsAPIView(ListAPIView):
    """
    API returns makes according to the search term and region
    POPULAR BRANDS and ALL MAKES
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        make_id = request.GET.get('make_id', None)
        search_term = ''
        if request.GET.get('term', None):
            search_term = request.GET.get('term')

        queryset = models.Model.objects.filter(
            make_id=make_id, name__istartswith=search_term
        ).order_by('name')
        serializer = serializers.ModelSerializer(queryset, many=True)
        # popular_models = queryset.filter(is_popular=True)
        # if popular_models.count() >= 9:
        #     popular_models = popular_models.all()[:9]
        # else:
        #     popular_models = popular_models.all()
        # popular_models_serializer = serializers.ModelSerializer(popular_models, many=True)
        return Response(status=status.HTTP_200_OK, data={
            'items': serializer.data,
            # 'popular': popular_models_serializer.data
        })


class FetchFeaturesAPIView(ListAPIView):
    """
    Returns the features according to vehicle type
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        vehicle_type = request.GET.get('vehicle_type', None)

        if vehicle_type:
            queryset = models.Feature.objects.filter(vehicle_type=vehicle_type)
        else:
            queryset = models.Feature.objects.all()

        queryset = queryset.order_by('name')
        serializer = serializers.FeatureSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


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


def process_makes(queryset):
    # results = []
    # for make in queryset:
    #     results.append({
    #         'id': make.id,
    #         'type': 'make',
    #         'text': make.name,
    #     })
    return list(map(lambda m: {
        'id': m.id, 'type': 'make', 'text': m.name
    }, queryset.all()))
    # return results


def process_models(queryset):
    # results = []
    # for model in queryset:
    #     results.append({
    #         'id': model.id,
    #         'type': 'model',
    #         'text': '{0} {1}'.format(model.make.name, model.name)
    #     })
    # return results
    return list(map(lambda m: {
        'id': m.id, 'type': 'model', 'text': '{0} {1}'.format(m.make.name, m.name)
    }, queryset.all()))


def process_results(queryset, source):
    if source == 'makes':
        return process_makes(queryset)

    if source == 'models':
        return process_models(queryset)


class AutocompleteAPIView(APIView):
    """
    Autocomplete API
    WARNING: Unstable code, needs to be improved
    """
    permission_classes = (AllowAny,)
    def get(self, request):
        term = request.GET.get('term', None)
        region_id = request.GET.get('region_id')

        makes = models.Make.objects.filter(name__istartswith=term)[:5]
        v_models = models.Model.objects.filter(
            Q(name__istartswith=term) | Q(make__name__istartswith=term), make__region_id=region_id
        ).select_related('make')[:5]

        results = process_results(makes, 'makes')
        results += process_results(v_models, 'models')
        return Response(status=status.HTTP_200_OK, data=results)


