import random

from django.conf import LazySettings
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.registration.views import RegisterView
from rest_auth.utils import jwt_encode
from rest_auth.views import LoginView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client

from accounts import models, serializers

settings = LazySettings()


class ProfileAPIView(APIView):
    """
    APIView for retrieving and updating user profiles
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProfileSerializer

    def get_object(self):
        return models.Profile.objects.filter(user_id=self.request.user.id).first()

    def get(self, request):
        instance = self.get_object()
        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance=instance)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def patch(self, request):
        instance = self.get_object()
        data = request.data
        serializer = self.serializer_class(instance=instance, data=data, partial=True)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        if 'user' in data and data['user'] != request.user.id:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={
                                'user': ['Invalid User ID']
                            })

        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class CustomLoginView(LoginView):
    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'token': self.token,
            }
            serializer = serializer_class(instance=data,
                                          context={'request': self.request})
        else:
            serializer = serializer_class(instance=self.token,
                                          context={'request': self.request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data['user'])
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        # Create Profile
        profile_data = request.data['profile']
        profile_data['user'] = user.id
        profile_serializer = serializers.ProfileSerializer(data=profile_data)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()
        headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class VerifyContactAPIView(APIView):
    """
    Verifies a phone number. Performs following checks:
    1. If user is logged in, check if phone number is associated with this user.
        - If associated, return OKAY.
        - If not associated, check:
            - If this phone number is associated with some other user, return BAD REQUEST.
            - Else send verification code.
    2. Else (Not logged in):
        - Check if phone number is associated with a user:
            - YES: Return ALREADY_ASSOCIATED
            - NO: Send verification code
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        if request.user.is_authenticated:
            pass
        else:
            data = request.data
            if 'phone_number' not in data:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'message': 'Phone number missing!'}
                )
            else:
                phone_number = data['phone_number']
                display_name = data.get('name', None)
                # TODO: Validate format, check if already associated with an
                #  account, else send verification code
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
                    user = create_temporary_user(phone_number, display_name)
                    message = client.messages.create(
                        body='Your Carnama verification code is {0}.'.format(user.verification_code),
                        to=phone_number,
                        from_=twilio_number
                    )
                    return Response(
                        status=status.HTTP_200_OK,
                        data={'message': 'Verification code sent to the provided '
                                         'contact number.'}
                    )


def create_temporary_user(phone_number, display_name=None):
    user = models.TemporaryUser(
        contact=phone_number,
        verification_code=generate_verification_code()
    )
    if display_name is not None:
        user.name = display_name
    user.save()
    return user


def generate_verification_code():
    code = ''
    for i in range(8):
        num = int(random.randint(0, 1))
        if num % 2 == 0:  # Append char
            code += chr(random.randint(ord('a'),ord('z')))
        else:  # Append digit
            code += str(random.randint(0, 9))

    return code


class VerifyCodeAPIView(APIView):
    """
    For verifying code sent to the user
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        serializer = serializers.VerifyCodeSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )

        temporary_user = models.TemporaryUser.objects.filter(
            contact=data['phone_number'], verification_code=data['code']
        ).first()

        if temporary_user is None:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'message': 'Invalid data provided.'
                }
            )

        temporary_user.is_verified = True
        temporary_user.save()

        # Create a new user with these credentials
        user_data = {
            'username': temporary_user.contact,
            'password1': temporary_user.verification_code,
            'password2': temporary_user.verification_code
        }
        user_serializer = RegisterSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save(request)

        profile = models.Profile(
            user_id=user.id,
            display_name=temporary_user.name,
            contact=temporary_user.contact
        ).save()

        token = jwt_encode(user)
        data = {
            'user': user,
            'token': token
        }
        serializer = serializers.JWTUserDetailsSerializer(instance=data)
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )


