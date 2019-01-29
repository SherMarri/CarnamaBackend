from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts import views



urlpatterns = [
    path('', include('accounts.rest_auth_urls')),
    path('registration/', include('rest_auth.registration.urls')),
    url('profile/$', view=views.ProfileAPIView.as_view(),
        name='accounts-profile'),
]