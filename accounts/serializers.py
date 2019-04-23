from rest_auth.serializers import JWTSerializer
from rest_framework import serializers

from accounts import models


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ('user', 'display_name', 'profile_type', 'is_banned')


class JWTUserDetailsSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = obj['user']
        data = {
            'username': user.username,
            'role': user.profile.get_profile_type_display(),
            'display_name': user.profile.display_name
        }
        return data


class VerifyCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=10)
