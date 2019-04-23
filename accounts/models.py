from django.contrib.auth import get_user_model
from django.db import models

from common.models import BaseModel

User = get_user_model()


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    ADMIN = 1
    AGENT = 2
    REGULAR = 3
    SHOWROOM = 4

    ProfileTypes = (
        (ADMIN, 'Admin'),
        (AGENT, 'Agent'),
        (REGULAR, 'Regular'),
        (SHOWROOM, 'Showroom')
    )

    profile_type = models.IntegerField(choices=ProfileTypes, default=REGULAR)
    display_name = models.CharField(max_length=128)
    contact = models.CharField(max_length=20, null=True, blank=True)
    # TODO: add display_image and integrate with S3 bucket
    is_banned = models.BooleanField(default=False, null=True, blank=True)


class TemporaryUser(BaseModel):
    name = models.CharField(max_length=20, null=True, blank=True, unique=True)
    contact = models.CharField(max_length=20, unique=True)
    verification_code = models.CharField(max_length=10)
    is_verified = models.BooleanField(default=False)
