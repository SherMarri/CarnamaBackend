from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts import models, serializers


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

        if 'user' in data and data['user']!=request.user.id:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={
                                'user': ['Invalid User ID']
                            })

        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)
