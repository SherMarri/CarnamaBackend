from django.conf.urls import url
from django.urls import include, path

from accounts import views

urlpatterns = [
    path('', include('accounts.rest_auth_urls')),
    path('registration/', views.CustomRegisterView.as_view(),
         name='accounts-register-user'),
    url('profile/$', view=views.ProfileAPIView.as_view(),
        name='accounts-profile'),
    url('verify_contact', view=views.VerifyContactAPIView.as_view(),
        name='accounts-verify-contact'),
    url('verify_code', view=views.VerifyCodeAPIView.as_view(),
        name='accounts-verify-code')
]