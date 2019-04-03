from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from transactions import views

router = DefaultRouter()
router.register('payments', views.PaymentViewSet, basename='transactions-payments')

urlpatterns = [
    path('', include(router.urls)),
]
