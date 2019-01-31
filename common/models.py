from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Region(models.Model):
    name = models.CharField(max_length=128)


class City(models.Model):
    name = models.CharField(max_length=128)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

