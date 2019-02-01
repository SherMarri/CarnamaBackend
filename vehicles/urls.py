from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from vehicles import views

router = DefaultRouter()
router.register('makes', views.MakeViewSet, basename='vehicles-make')
router.register('models', views.ModelViewSet, basename='vehicles-model')
router.register('variants', views.VariantViewSet, basename='vehicles-variant')
router.register('features', views.FeatureViewSet, basename='vehicles-feature')

urlpatterns = [
    path('', include(router.urls)),
    url('search/$', view=views.AutocompleteAPIView.as_view(), name='listings-new'),
]
