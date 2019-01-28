from rest_framework import serializers

from accounts import models


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ('user', 'display_name', 'profile_type')
