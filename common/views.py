from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from common import models, serializers


class FetchCitiesAPIView(ListAPIView):
    """
    API returns makes according to the search term and region
    POPULAR BRANDS and ALL MAKES
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        region = request.GET.get('region', None)
        queryset = models.City.objects.filter(region__name=region)
        serializer = serializers.CitySerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
