from django.urls import path
from .views import (
    ApplicationCreateView, ApplicationListView, ApplicationDetailView,
    ApplicationUpdateView, MyApplicationsView, withdraw_application_view,
    application_stats_view
)

urlpatterns = [
    path('apply/', ApplicationCreateView.as_view(), name='application-create'),
    path('', ApplicationListView.as_view(), name='application-list'),
    path('my-applications/', MyApplicationsView.as_view(), name='my-applications'),
    path('stats/', application_stats_view, name='application-stats'),
    path('<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
    path('<int:pk>/update/', ApplicationUpdateView.as_view(), name='application-update'),
    path('<int:application_id>/withdraw/', withdraw_application_view, name='withdraw-application'),
]