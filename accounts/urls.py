from django.conf.urls import url
from django.urls import include


urlpatterns = [
    url('rest-auth/', include('rest_auth.urls')),
    url('rest-auth/registration/', include('rest_auth.registration.urls'))
]