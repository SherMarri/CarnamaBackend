from django.db import models

from common.models import Region, BaseModel

CAR = 1
BIKE = 2

VEHICLE_TYPES = (
    (CAR, "Car"),
    (BIKE, "Bike")
)


class Make(BaseModel):
    name = models.CharField(max_length=128)
    vehicle_type = models.IntegerField(choices=VEHICLE_TYPES)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    is_popular = models.BooleanField(null=True, default=False)


class Model(BaseModel):
    name = models.CharField(max_length=128)
    make = models.ForeignKey(Make, on_delete=models.CASCADE)
    is_popular = models.BooleanField(null=True, default=False)


class Variant(BaseModel):
    name = models.CharField(max_length=128)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)


class Feature(BaseModel):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=500, null=True, blank=True)
    vehicle_type = models.IntegerField(choices=VEHICLE_TYPES)


class Result(object):
    def __init__(self):
        pass

    def get_json_representation(self):
        pass


class MakeResult(Result):
    def __init__(self, make):
        super().__init__()
        self.make = make

    def get_json_representation(self):
        result = {
            'id': self.make.id,
            'type': 'make',
            'text': self.make.name,
            'vehicle_type': self.make.vehicle_type
        }
        return result


class ModelResult(Result):
    def __init__(self, result_type, model):
        super().__init__(result_type)
        self.model = model

    def get_json_representation(self):
        result = {
            'id': self.model.id,
            'type': 'model',
            'text': '{0} {1}'.format(self.model.make.name, self.model.name)
        }
        return result


class VariantResult(Result):
    def __init__(self, result_type, variant):
        super().__init__(result_type)
        self.variant = variant

    def get_json_representation(self):
        result = {
            'id': self.variant.id,
            'type': 'variant',
            'text': '{0} {1} {2}'.format(
                self.variant.model.make.name, self.variant.model.name,
                self.variant.name)
        }
        return result
