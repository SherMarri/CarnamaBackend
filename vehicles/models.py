from django.db import models

from common.models import Region

CAR = 1
BIKE = 2

VEHICLE_TYPES = (
    (CAR, "Car"),
    (BIKE, "Bike")
)


class Make(models.Model):
    name = models.CharField(max_length=128)
    vehicle_type = models.IntegerField(choices=VEHICLE_TYPES)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)


class Model(models.Model):
    name = models.CharField(max_length=128)
    make = models.ForeignKey(Make, on_delete=models.CASCADE)


class Variant(models.Model):
    name = models.CharField(max_length=128)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)


class Feature(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=500, null=True, blank=True)
    vehicle_type = models.IntegerField(choices=VEHICLE_TYPES)

