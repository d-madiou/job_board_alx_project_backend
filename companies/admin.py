# companies/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'logo_thumbnail', 'location', 'industry', 'size', 
        'is_verified', 'job_count_display', 'created_at'
    ]
    list_filter = ['is_verified', 'size', 'industry', 'created_at']
    search_fields = ['name', 'description', 'location', 'industry']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'job_count_display', 'logo_preview']
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'slug', 'description']
        }),
        ('Logo', {
            'fields': ['logo', 'logo_url', 'logo_preview'],
            'description': 'Upload a logo file or provide an external logo URL. Uploaded file takes priority.'
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
    
    def logo_thumbnail(self, obj):
        """Display small logo thumbnail in list view"""
        logo_url = obj.logo_display_url
        if logo_url:
            return format_html(
                '<img src="{}" width="40" height="40" style="object-fit: cover; border-radius: 4px;" />',
                logo_url
            )
        return format_html('<span style="color: #999;">No logo</span>')
    logo_thumbnail.short_description = 'Logo'
    
    def logo_preview(self, obj):
        """Display larger logo preview in detail view"""
        logo_url = obj.logo_display_url
        if logo_url:
            return format_html(
                '''
                <div style="margin: 10px 0;">
                    <img src="{}" style="max-width: 200px; max-height: 200px; object-fit: contain; border: 1px solid #ddd; border-radius: 8px;" />
                    <br><small style="color: #666;">Current logo</small>
                </div>
                ''',
                logo_url
            )
        return format_html('<span style="color: #999;">No logo uploaded</span>')
    logo_preview.short_description = 'Logo Preview'
    
    def job_count_display(self, obj):
        """Display job count with styling"""
        count = obj.job_count
        if count > 0:
            return format_html(
                '<span style="color: green; font-weight: bold;">{}</span>',
                count
            )
        return '0'
    job_count_display.short_description = 'Active Jobs'
    
    # Custom actions
    actions = ['mark_as_verified', 'mark_as_unverified']
    
    def mark_as_verified(self, request, queryset):
        """Mark selected companies as verified"""
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} companies marked as verified.')
    mark_as_verified.short_description = 'Mark selected companies as verified'
    
    def mark_as_unverified(self, request, queryset):
        """Mark selected companies as unverified"""
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} companies marked as unverified.')
    mark_as_unverified.short_description = 'Mark selected companies as unverified'
    
    # Optimize database queries
    def get_queryset(self, request):
        """Optimize queryset to reduce database hits"""
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('jobs')
    
    class Media:
        """Add custom CSS/JS for better admin styling"""
        css = {
            'all': ('admin/css/company_admin.css',)  # Optional: create custom CSS
        }
        
    # Optional: Add custom form validation
    def clean(self, form):
        """Custom form validation"""
        cleaned_data = super().clean(form)
        
        # Ensure at least one logo source is provided if company is verified
        if cleaned_data.get('is_verified'):
            logo = cleaned_data.get('logo')
            logo_url = cleaned_data.get('logo_url')
            
            if not logo and not logo_url:
                form.add_error(None, 
                    "Verified companies should have a logo. Please upload a logo file or provide a logo URL."
                )
        
        return cleaned_data