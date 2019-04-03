from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from listings import views

router = DefaultRouter()
router.register('autosale_requests', viewset=views.AutosaleRequestViewSet,
                base_name='listings-autosale-requests')
router.register('daily_ad_views', viewset=views.DailyAdViewsViewSet,
                base_name='listings-daily-ad-views')
router.register('saved_searches', viewset=views.SavedSearchViewSet,
                base_name='listings-saved-searches')
router.register('callbacks', viewset=views.CallbackViewSet,
                base_name='listings-callbacks')
router.register('reported_ads', viewset=views.ReportedAdViewSet,
                base_name='listings-reported-ads')
urlpatterns = [
    url('new/$', view=views.PostAdAPIView.as_view(), name='listings-new'),
    url('(?P<id>\d+)', view=views.FetchAdAPIView.as_view(), name='listings-detail'),
    url('', include(router.urls)),
    url('get_presigned_urls', view=views.GetPresignedUrlsAPIView.as_view(), name='get-presigned-urls')
]
