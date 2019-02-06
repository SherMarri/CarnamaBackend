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

    PENDING = 1
    APPROVED = 2
    REJECTED = 3
    EXPIRED = 4
    AD_STATUS_CHOICES = (
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
        (EXPIRED, "Expired"),
    )
    status = models.IntegerField(choices=AD_STATUS_CHOICES, default=PENDING)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)


class AutosaleRequest(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    model = models.ForeignKey(v_models.Model, on_delete=models.CASCADE)
    year = models.IntegerField()
    color = models.CharField(max_length=20)
    name = models.CharField(max_length=120)
    contact = models.CharField(max_length=20)

    PENDING = 1
    PROCESSING = 2
    COMPLETED = 3
    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (PROCESSING, "Processing"),
        (COMPLETED, "Completed"),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)


class FavoritedAd(BaseModel):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class DailyAdViews(BaseModel):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    date = models.DateField()
    views = models.IntegerField(default=0)


class SavedSearch(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.ForeignKey(v_models.Make, on_delete=models.CASCADE,
                              null=True, blank=True)
    model = models.ForeignKey(v_models.Model, on_delete=models.CASCADE,
                              null=True, blank=True)
    variant = models.ForeignKey(v_models.Variant, on_delete=models.CASCADE,
                                null=True, blank=True)


class Callback(BaseModel):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    contact = models.CharField(max_length=20)

    PENDING = 1
    COMPLETED = 2
    CALLBACK_STATUS_CHOICES = (
        (PENDING, "Pending"),
        (COMPLETED, "Completed")
    )
    status = models.IntegerField(choices=CALLBACK_STATUS_CHOICES, default=PENDING)


class ReportedAd(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    DUPLICATE = 1
    SPAM = 2
    RESELLER = 3
    WRONG_CATEGORY = 4
    PHONE_NOT_AVAILABLE = 5
    REASON_CHOICES = (
        (DUPLICATE, "Duplicate"),
        (SPAM, "Spam"),
        (RESELLER, "Reseller"),
        (WRONG_CATEGORY, "Wrong category"),
        (PHONE_NOT_AVAILABLE, "Phone not available")
    )
    reason = models.IntegerField(choices=REASON_CHOICES)
    total_reports = models.IntegerField(default=1)
    is_banned = models.BooleanField(default=False)
