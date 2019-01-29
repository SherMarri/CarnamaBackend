from django.contrib.auth import get_user_model
from django.db import models

from common.models import City, BaseModel
from vehicles.models import Variant, Feature

User = get_user_model()


class Ad(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    year = models.IntegerField()
    color = models.CharField(max_length=20)
    mileage = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=128, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    price = models.FloatField()
    contact = models.CharField(max_length=20)
    description = models.TextField()


class AdFeatures(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
