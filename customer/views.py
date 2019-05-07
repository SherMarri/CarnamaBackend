from django.conf import LazySettings
from django.core.paginator import Paginator
from django.db.models import Count, Q
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client

from accounts.models import Profile, User, VerificationCode
from accounts.serializers import ProfileSerializer
from accounts.views import generate_verification_code
from listings import models as listings_models
from listings.serializers import AdDetailsSerializer, FavoritedAdSerializer

settings = LazySettings()


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
        my_ads_total = my_ads = listings_models.Ad.objects.filter(
            user_id=request.user.id
        ).count()
        my_ads = listings_models.Ad.objects.filter(
            user_id=request.user.id
        ).select_related('model').prefetch_related('photos').order_by(
            '-created_at'
        )[:3]
        my_ads_serializer = AdDetailsSerializer(my_ads, many=True)

        # Fetch top 5 favorited ads
        favorited_ads_total = listings_models.FavoritedAd.objects.filter(
            user_id=request.user.id
        ).count()
        favorited_ads = listings_models.FavoritedAd.objects.filter(
            user_id=request.user.id
        ).select_related('ad__model')[:3]
        favorited_ads_serializer = FavoritedAdSerializer(favorited_ads, many=True)

        response_data = {
            'my_ads': {
                'items': my_ads_serializer.data,
                'count': my_ads_total
            },
            'favorited_ads': {
                'items': favorited_ads_serializer.data,
                'count': favorited_ads_total
            }
        }
        return Response(status=status.HTTP_200_OK, data=response_data)


class UserAdsAPIView(APIView):
    """
    APIView that returns data for manage ads page on dashboard
    """
    permission_classes = (IsCustomer,)

    def get(self, request):
        params = self.request.GET
        queryset = listings_models.Ad.objects.filter(
            user_id=request.user.id).select_related('model').prefetch_related(
            'photos'
        ).annotate(
            favorited=Count('favorited_ads', filter=Q(favorited_ads__user_id=request.user.id))
        ).order_by('-created_at')
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

        serializer = AdDetailsSerializer(results, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data={
                'items': serializer.data,
                'page': results.number,
                'total_pages': paginator.num_pages,
                'count': paginator.count
            }
        )


class FavoritedAdsAPIView(APIView):
    """
    APIView that returns data for favorited ads page on dashboard
    """
    permission_classes = (IsCustomer,)

    def get(self, request):
        params = self.request.GET
        queryset = listings_models.Ad.objects.filter(
            favorited_ads__user_id=request.user.id
        ).annotate(
            favorited=Count('favorited_ads', filter=Q(favorited_ads__user_id=request.user.id))
        ).select_related('model', 'city').prefetch_related(
            'photos', 'features'
        ).order_by('-created_at')

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

        serializer = AdDetailsSerializer(results, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data={
                'items': serializer.data,
                'page': results.number,
                'total_pages': paginator.num_pages,
                'count': paginator.count
            }
        )


class UserSettingsAPIView(APIView):
    """
    APIView for getting and setting user profile settings
    """
    permission_classes = (IsCustomer,)

    def get(self, request):
        profile = Profile.objects.filter(user_id=request.user.id).first()
        if not profile:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(instance=profile)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request):
        data = request.data
        user = request.user

        profile = user.profile


        if 'display_name' in data:
            profile.display_name = data['display_name']

        if 'contact' in data:
            contact = data['contact']

            v_code = VerificationCode.objects.filter(
                user_id=user.id, contact=contact, is_verified=True
            ).last()

            if v_code is None:
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={
                                    'message': 'Contact not verified'
                                })
            else:
                profile.contact = contact

        profile.save()

        if 'password1' in data and 'password2' in data and 'current_password' in data:
            if not user.check_password(data['current_password']):
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={
                                    'message': 'Your existing password is invalid.'
                                })

            if data['password1'] == data['password2']:
                user.set_password(data['password1'])
                user.save()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={
                                    'message': 'New passwords do not match,'
                                })

        serializer = ProfileSerializer(instance=profile)
        return Response(status=status.HTTP_200_OK, data=serializer.data)



class VerifyContactAPIView(APIView):
    """
    Verifies a phone number. Performs following checks:
    Not logged in:
        - Check if phone number is associated with a user:
            - YES: Return ALREADY_ASSOCIATED
            - NO: Send verification code
    """
    permission_classes = (IsCustomer,)

    def post(self, request):
        data = request.data
        if 'contact' not in data:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': 'Contact missing!'}
            )
        else:
            phone_number = data['contact']
            user = request.user
            # TODO: Validate format, check if already associated with an
            #  account, else send verification code
            if User.objects.filter(username=phone_number).exists():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        'code': 'USER_EXISTS',
                        'message': 'A user with this phone number already exists.'
                    }
                )
            sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
            auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
            twilio_number = getattr(settings, 'TWILIO_PHONE_NUMBER', None)
            if sid is None or auth_token is None or twilio_number is None:
                return Response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    data={'message': 'Something unexpected occurred, '
                                     'please contact Carnama support team!'}
                )
            else:
                client = Client(sid, auth_token)
                VerificationCode(
                    user_id=user.id, contact=phone_number,
                    verification_code=generate_verification_code()
                ).save()
                # message = client.messages.create(
                #     body='Your Carnama Verification Code is: {0}.'.format(v_code.verification_code),
                #     to=phone_number,
                #     from_=twilio_number
                # )
                return Response(
                    status=status.HTTP_200_OK,
                    data={'message': 'Verification code sent to the provided '
                                     'contact number.'}
                )


class VerifyCodeAPIView(APIView):
    permission_classes = (IsCustomer,)

    def post(self, request):
        data = request.data
        if 'code' not in data or 'contact' not in data:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'message': 'Mobile number or verification code is missing.'
                })

        v_code = VerificationCode.objects.filter(
            user_id=request.user.id, verification_code=data['code'],
            contact=data['contact']
        ).last()

        if not v_code:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'message': 'Failed to verify code.'
                }
            )

        v_code.is_verified = True
        v_code.save()

        return Response(
            status=status.HTTP_200_OK,
            data={'contact': v_code.contact}
        )
