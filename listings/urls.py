from django.conf.urls import url

from listings import views

urlpatterns = [
    url('new/$', view=views.PostAdAPIView.as_view(),
        name='listings-new'),
]
