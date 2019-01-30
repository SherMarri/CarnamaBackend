from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from vehicles import views

router = DefaultRouter()
router.register('make', views.MakeViewSet, basename='vehicles-make')
router.register('model', views.ModelViewSet, basename='vehicles-model')
router.register('variant', views.VariantViewSet, basename='vehicles-variant')
router.register('feature', views.FeatureViewSet, basename='vehicles-feature')

urlpatterns = [
    path('', include(router.urls)),
]
