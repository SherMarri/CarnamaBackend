from django.conf.urls import url
from django.urls import include, path

from common import views

urlpatterns = [
    url('fetch-cities/$', view=views.FetchCitiesAPIView.as_view(),
        name='fetch-cities'),
]
