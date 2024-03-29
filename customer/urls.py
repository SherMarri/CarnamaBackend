from django.conf.urls import url
from customer import views

urlpatterns = [
    url('dashboard_summary', view=views.DashboardSummaryAPIView.as_view(), name='customer-dashboard-summary'),
    url('ads', view=views.UserAdsAPIView.as_view(), name='customer-ads'),
    url('favorites', view=views.FavoritedAdsAPIView.as_view(), name='customer-favorites'),
    url('settings', view=views.UserSettingsAPIView.as_view(), name='customer-settings'),
    url('verify_contact', view=views.VerifyContactAPIView.as_view(), name='customer-verify-contact'),
    url('verify_code', view=views.VerifyCodeAPIView.as_view(), name='customer-verify-code')
]
