from django.urls import path
from .views import (
    CompanyListView, CompanyCreateView, CompanyDetailView, CompanyUpdateDeleteView
)

urlpatterns = [
    path('', CompanyListView.as_view(), name='company-list'),
    path('create/', CompanyCreateView.as_view(), name='company-create'),
    path('api/companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('<slug:slug>/edit/', CompanyUpdateDeleteView.as_view(), name='company-update-delete'),
]