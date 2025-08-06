# applications/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'applicant_name', 'job_title', 'company_name', 'status',
        'years_of_experience', 'expected_salary', 'applied_at'
    ]
    list_filter = [
        'status', 'applied_at', 'job__company', 'job__category',
        'years_of_experience'
    ]
    search_fields = [
        'applicant__first_name', 'applicant__last_name',
        'applicant__email', 'job__title', 'job__company__name'
    ]
    readonly_fields = ['applied_at', 'updated_at']
    raw_id_fields = ['job', 'applicant']
    
    fieldsets = [
        ('Application Info', {
            'fields': ['job', 'applicant', 'status', 'applied_at', 'updated_at']
        }),
        ('Application Content', {
            'fields': ['cover_letter', 'resume_url', 'portfolio_url', 'linkedin_url']
        }),
        ('Contact Information', {
            'fields': ['phone', 'email']
        }),
        ('Additional Info', {
            'fields': [
                'years_of_experience', 'expected_salary', 'availability_date'
            ]
        }),
        ('Admin Notes', {
            'fields': ['admin_notes', 'rejection_reason', 'reviewed_at'],
            'classes': ['collapse']
        })
    ]
    
    actions = [
        'mark_as_reviewed', 'mark_as_shortlisted', 'mark_as_interviewed',
        'mark_as_rejected', 'mark_as_accepted'
    ]
    
    def applicant_name(self, obj):
        return obj.applicant.get_full_name()
    applicant_name.short_description = 'Applicant'
    applicant_name.admin_order_field = 'applicant__first_name'
    
    def job_title(self, obj):
        url = reverse('admin:jobs_job_change', args=[obj.job.pk])
        return format_html('<a href="{}">{}</a>', url, obj.job.title)
    job_title.short_description = 'Job'
    job_title.admin_order_field = 'job__title'
    
    def company_name(self, obj):
        return obj.job.company.name
    company_name.short_description = 'Company'
    company_name.admin_order_field = 'job__company__name'
    
    def mark_as_reviewed(self, request, queryset):
        updated = queryset.update(status='reviewed')
        self.message_user(request, f'{updated} applications marked as reviewed.')
    mark_as_reviewed.short_description = 'Mark as reviewed'
    
    def mark_as_shortlisted(self, request, queryset):
        updated = queryset.update(status='shortlisted')
        self.message_user(request, f'{updated} applications shortlisted.')
    mark_as_shortlisted.short_description = 'Mark as shortlisted'
    
    def mark_as_interviewed(self, request, queryset):
        updated = queryset.update(status='interviewed')
        self.message_user(request, f'{updated} applications marked as interviewed.')
    mark_as_interviewed.short_description = 'Mark as interviewed'
    
    def mark_as_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} applications rejected.')
    mark_as_rejected.short_description = 'Reject applications'
    
    def mark_as_accepted(self, request, queryset):
        updated = queryset.update(status='accepted')
        self.message_user(request, f'{updated} applications accepted.')
    mark_as_accepted.short_description = 'Accept applications'