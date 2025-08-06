# companies/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import datetime
import os

def company_logo_upload_path(instance, filename):
    """Generate upload path for company logos"""
    # Get file extension
    ext = filename.split('.')[-1]
    # Create filename: company_slug.extension
    filename = f"{instance.slug}.{ext}"
    # Return the upload path
    return f'company_logos/{filename}'

class Company(models.Model):
    SIZE_CHOICES = [
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('501-1000', '501-1000 employees'),
        ('1000+', '1000+ employees'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    
    # Replace logo_url with logo ImageField for file uploads
    logo = models.ImageField(
        upload_to=company_logo_upload_path, 
        blank=True, 
        null=True,
        help_text="Company logo image"
    )
    # Keep logo_url as fallback for external URLs (optional)
    logo_url = models.URLField(blank=True, help_text="External logo URL (used if no logo file uploaded)")
    
    location = models.CharField(max_length=255, blank=True)
    size = models.CharField(max_length=50, choices=SIZE_CHOICES, blank=True)
    founded_year = models.IntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(1800), MaxValueValidator(datetime.date.today().year)]
    )
    industry = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # Social Media Links
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'companies'
        verbose_name_plural = 'companies'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def job_count(self):
        return self.jobs.filter(is_active=True).count()
    
    @property
    def logo_display_url(self):
        """Return logo URL - either from uploaded file or external URL"""
        if self.logo:
            return self.logo.url
        elif self.logo_url:
            return self.logo_url
        return None
    
    def delete(self, *args, **kwargs):
        """Override delete to remove logo file when company is deleted"""
        if self.logo:
            # Delete the file from storage
            if os.path.isfile(self.logo.path):
                os.remove(self.logo.path)
        super().delete(*args, **kwargs)