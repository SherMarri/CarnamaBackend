from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from listings import models as listings_models
from listings.serializers import AdDetailsSerializer, FavoritedAdSerializer


class IsCustomer(BasePermission):
    """
    Allows access only to customers.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and
            request.user.profile.profile_type == request.user.profile.REGULAR)


class DashboardSummaryAPIView(APIView):
    """
    APIView that returns data for customer dashboard:
        1. My Ads
        2. My Favorites
        3. Total Spent
        4. Saved Searches
        5. Views
        6. Messages
    """
    permission_classes = (IsCustomer,)

    def get(self, request):
        response_data = None

        # Fetch top 5 ads by this user
        my_ads = listings_models.Ad.objects.filter(
            user_id=request.user.id
        ).select_related('model').prefetch_related('features').order_by(
            '-created_at'
        )[:5]
        my_ads_serializer = AdDetailsSerializer(my_ads, many=True)

        # Fetch top 5 favorited ads
        favorited_ads = listings_models.FavoritedAd.objects.filter(
            user_id=request.user.id
        ).select_related('ad__model')
        favorited_ads_serializer = FavoritedAdSerializer(favorited_ads, many=True)

        response_data = {
            'my_ads': my_ads_serializer.data,
            'favorited_ads': favorited_ads_serializer.data
        }
        return Response(status=status.HTTP_200_OK, data=response_data)
