import datetime

from django.contrib.auth import get_user_model
from django.db import models

from common.models import City, BaseModel
from vehicles import models as v_models

User = get_user_model()


class Ad(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    variant = models.ForeignKey(v_models.Variant, on_delete=models.SET_NULL,
                                null=True, blank=True)
    model = models.ForeignKey(v_models.Model, on_delete=models.SET_NULL,
                              null=True, blank=True)
    year = models.IntegerField()
    color = models.CharField(max_length=20)
    mileage = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=128, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE,
                             related_name='ads')
    registration_city = models.ForeignKey(City, on_delete=models.CASCADE,
                                          related_name='registered_vehicle_ads')
    price = models.FloatField()
    contact = models.CharField(max_length=20)
    contact_person = models.CharField(max_length=128)
    comments = models.TextField(null=True, blank=True)
    features = models.ManyToManyField(v_models.Feature, related_name='ads')
    views = models.IntegerField(default=0)
    youtube_link = models.CharField(max_length=128, null=True, blank=True)

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

    SEDAN = 1
    CABRIOLET = 2
    WAGON = 3
    BODY_TYPES = (
        (SEDAN, "Sedan"),
        (CABRIOLET, "Cabriolet"),
        (WAGON, "Wagon")
    )
    body_type = models.IntegerField(choices=BODY_TYPES)
    right_handed_drive = models.BooleanField(default=True)

    MANUAL = 1
    AUTOMATIC = 2
    CVT = 3
    SEMI_AUTOMATIC = 4
    TRANSMISSION_TYPES = (
        (MANUAL, "Manual"),
        (AUTOMATIC, "Automatic"),
        (CVT, "CVT"),
        (SEMI_AUTOMATIC, "Semi-automatic")
    )
    transmission_type = models.IntegerField(choices=TRANSMISSION_TYPES)

    MODIFICATION_1_8 = 1
    MODIFICATION_2_0 = 2
    MODIFICATION_2_5 = 3
    MODIFICATION_3_5 = 4
    MODIFICATION_5_5 = 5
    MODIFICATION_TYPES = (
        (MODIFICATION_1_8, "1.8 L"),
        (MODIFICATION_2_0, "2.0 L"),
        (MODIFICATION_2_5, "2.5 L"),
        (MODIFICATION_3_5, "3.5 L"),
        (MODIFICATION_5_5, "5.5 L")
    )
    modification_type = models.IntegerField(choices=MODIFICATION_TYPES)

    PETROL = 1
    DIESEL = 2
    FUEL_TYPES = (
        (PETROL, 'Petrol'),
        (DIESEL, 'Diesel')
    )
    fuel_type = models.IntegerField(choices=FUEL_TYPES)
    gas_equipment = models.BooleanField(default=False)

    ASSEMBLY_PAKISTAN = 1
    ASSEMBLY_IMPORTED = 2
    ASSEMBLY_TYPES = (
        (ASSEMBLY_PAKISTAN, 'Pakistan'),
        (ASSEMBLY_IMPORTED, 'Imported')
    )
    assembly_type = models.IntegerField(choices=ASSEMBLY_TYPES)

    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)


class AdPhoto(BaseModel):
    ad = models.ForeignKey(Ad, on_delete=models.SET_NULL, null=True,
                           blank=True, related_name='photos')
    uuid = models.CharField(max_length=128)


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
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE,
                           related_name='favorited_ads')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class DailyAdViews(BaseModel):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE,
                           related_name='daily_views')
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
