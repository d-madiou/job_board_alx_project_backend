# jobs/filters.py
import django_filters
from django.db import models
from .models import Job

class JobFilter(django_filters.FilterSet):
    location = django_filters.CharFilter(lookup_expr='icontains')
    salary_min = django_filters.NumberFilter(field_name='salary_min', lookup_expr='gte')
    salary_max = django_filters.NumberFilter(field_name='salary_max', lookup_expr='lte')
    company = django_filters.NumberFilter(field_name='company__id')
    category = django_filters.NumberFilter(field_name='category__id')
    skills = django_filters.CharFilter(field_name='skills_required', lookup_expr='icontains')
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = Job
        fields = {
            'job_type': ['exact'],
            'experience_level': ['exact'],
            'is_remote': ['exact'],
            'remote_type': ['exact'],
            'is_featured': ['exact'],
            'is_urgent': ['exact'],
        }