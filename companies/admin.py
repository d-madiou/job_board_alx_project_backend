from django.contrib import admin
from django.utils.html import format_html
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'location', 'industry', 'size', 'is_verified', 
        'job_count_display', 'created_at'
    ]
    list_filter = ['is_verified', 'size', 'industry', 'created_at']
    search_fields = ['name', 'description', 'location', 'industry']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'job_count_display']
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'slug', 'description', 'logo_url']
        }),
        ('Contact Information', {
            'fields': ['website', 'email', 'phone', 'location']
        }),
        ('Company Details', {
            'fields': ['size', 'founded_year', 'industry', 'is_verified']
        }),
        ('Social Media', {
            'fields': ['linkedin_url', 'twitter_url', 'facebook_url'],
            'classes': ['collapse']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
    
    def job_count_display(self, obj):
        count = obj.job_count
        if count > 0:
            return format_html(
                '<span style="color: green; font-weight: bold;">{}</span>',
                count
            )
        return '0'
    job_count_display.short_description = 'Active Jobs'
    
    actions = ['mark_as_verified', 'mark_as_unverified']
    
    def mark_as_verified(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} companies marked as verified.')
    mark_as_verified.short_description = 'Mark selected companies as verified'
    
    def mark_as_unverified(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} companies marked as unverified.')
    mark_as_unverified.short_description = 'Mark selected companies as unverified'