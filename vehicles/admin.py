from django.contrib import admin


class MakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'vehicle_type', 'region')


class ModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'make')


class VariantAdmin(admin.ModelAdmin):
    list_display = ('name', 'model')


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'vehicle_type')
