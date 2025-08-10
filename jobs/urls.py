from django.urls import path
from .views import (
    CategoryListView, CategoryCreateView,
    JobListView, JobCreateView, JobDetailView, JobUpdateDeleteView,
    featured_jobs_view, recent_jobs_view, job_stats_view
)

urlpatterns = [
   
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    
    path('', JobListView.as_view(), name='job-list'),
    path('create/', JobCreateView.as_view(), name='job-create'),
    path('featured/', featured_jobs_view, name='featured-jobs'),
    path('recent/', recent_jobs_view, name='recent-jobs'),
    path('stats/', job_stats_view, name='job-stats'),
    path('<slug:slug>/', JobDetailView.as_view(), name='job-detail'),
    path('<slug:slug>/edit/', JobUpdateDeleteView.as_view(), name='job-update-delete'),
]