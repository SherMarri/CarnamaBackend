from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from accounts import views


router = DefaultRouter()
router.register('profile', viewset=views.ProfileViewSet)

urlpatterns = [
    url('', include('accounts.rest_auth_urls')),
    url('registration/', include('rest_auth.registration.urls')),
    url('', include(router.urls)),
]