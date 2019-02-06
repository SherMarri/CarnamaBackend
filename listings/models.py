from django.contrib.auth import get_user_model
from django.db import models

from common.models import City, BaseModel
from vehicles import models as v_models

User = get_user_model()


class Ad(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    variant = models.ForeignKey(v_models.Variant, on_delete=models.SET_NULL,
                                null=True, blank=True)
    model = models.ForeignKey(v_models.Model, on_delete=models.SET_NULL,
                              null=True, blank=True)
    year = models.IntegerField()
    color = models.CharField(max_length=20)
    mileage = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=128, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    price = models.FloatField()
    contact = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    features = models.ManyToManyField(v_models.Feature, related_name='ads')
    views = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
