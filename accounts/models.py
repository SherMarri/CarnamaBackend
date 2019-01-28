from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    ADMIN = 1
    AGENT = 2
    REGULAR = 3
    SHOWROOM = 4

    ProfileTypes = (
        ('Admin', ADMIN),
        ('Agent', AGENT),
        ('Regular', REGULAR),
        ('Showroom', SHOWROOM)
    )

    profile_type = models.IntegerField(choices=ProfileTypes)
    display_name = models.CharField(max_length=128)
    # TODO: add display_image and integrate with S3 bucket
