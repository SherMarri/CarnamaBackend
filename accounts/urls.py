from django.conf.urls import url
from django.urls import include


urlpatterns = [
    url('', include('accounts.rest_auth_urls')),
    url('registration/', include('rest_auth.registration.urls'))
]