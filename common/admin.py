from django.contrib import admin

from common import models


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')


admin.site.register(models.Region, RegionAdmin)
admin.site.register(models.City, CityAdmin)
