from django.db import models

from common.models import BaseModel
from listings.models import Ad


class Payment(BaseModel):
    order_id = models.CharField(max_length=128, unique=True)
    ad = models.ForeignKey(Ad, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.FloatField()

    FEATURED = 1
    AUTOSALE = 2
    PACKAGE_CHOICES = (
        (FEATURED, "Featured"),
        (AUTOSALE, "Autosale")
    )

    package = models.IntegerField(choices=PACKAGE_CHOICES)
