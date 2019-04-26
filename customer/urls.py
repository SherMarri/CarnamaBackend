from django.conf.urls import url
from customer import views

urlpatterns = [
    url('dashboard_summary', view=views.DashboardSummaryAPIView.as_view(), name='customer-dashboard-summary')
]
