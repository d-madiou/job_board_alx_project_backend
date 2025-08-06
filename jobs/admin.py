# jobs/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count

from companies import models
from .models import Job, Category
from django.db.models import Count, Q

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'job_count_display', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'job_count_display']
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            job_count=Count('jobs', filter=models.Q(jobs__is_active=True))
        )
    
    def job_count_display(self, obj):
        return obj.job_count if hasattr(obj, 'job_count') else obj.job_count
    job_count_display.short_description = 'Active Jobs'
    job_count_display.admin_order_field = 'job_count'

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'company', 'category', 'job_type', 'experience_level',
        'location', 'is_remote', 'status', 'is_featured', 'views_count',
        'applications_count', 'created_at'
    ]
    list_filter = [
        'status', 'job_type', 'experience_level', 'is_remote', 'is_featured',
        'is_urgent', 'category', 'created_at'
    ]
    search_fields = ['title', 'description', 'company__name', 'skills_required']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = [
        'slug', 'views_count', 'applications_count', 'created_at',
        'updated_at', 'is_expired'
    ]
    raw_id_fields = ['company', 'posted_by']
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['title', 'slug', 'description', 'company', 'category', 'posted_by']
        }),
        ('Job Details', {
            'fields': [
                'requirements', 'responsibilities', 'benefits',
                'job_type', 'experience_level', 'skills_required'
            ]
        }),
        ('Location & Remote', {
            'fields': ['location', 'is_remote', 'remote_type']
        }),
        ('Salary Information', {
            'fields': [
                'salary_min', 'salary_max', 'salary_currency',
                'salary_type', 'show_salary'
            ],
            'classes': ['collapse']
        }),
        ('Application Settings', {
            'fields': [
                'accept_applications', 'application_url', 'application_email'
            ]
        }),
        ('Status & Visibility', {
            'fields': [
                'status', 'is_active', 'is_featured', 'is_urgent', 'expires_at'
            ]
        }),
        ('Statistics', {
            'fields': ['views_count', 'applications_count'],
            'classes': ['collapse']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
    
    actions = ['mark_as_featured', 'mark_as_urgent', 'deactivate_jobs', 'activate_jobs']
    
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} jobs marked as featured.')
    mark_as_featured.short_description = 'Mark selected jobs as featured'
    
    def mark_as_urgent(self, request, queryset):
        updated = queryset.update(is_urgent=True)
        self.message_user(request, f'{updated} jobs marked as urgent.')
    mark_as_urgent.short_description = 'Mark selected jobs as urgent'
    
    def deactivate_jobs(self, request, queryset):
        updated = queryset.update(is_active=False, status='paused')
        self.message_user(request, f'{updated} jobs deactivated.')
    deactivate_jobs.short_description = 'Deactivate selected jobs'
    
    def activate_jobs(self, request, queryset):
        updated = queryset.update(is_active=True, status='active')
        self.message_user(request, f'{updated} jobs activated.')
    activate_jobs.short_description = 'Activate selected jobs'