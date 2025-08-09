# jobs/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from companies.models import Company

User = get_user_model()

class Category(models.Model):
    '''I will implement the model category in this part'''
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def job_count(self):
        return self.jobs.filter(is_active=True).count()

class Job(models.Model):
    '''I will define all the models of the Job here'''
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
    ]
    
    EXPERIENCE_CHOICES = [
        ('entry_level', 'Entry Level'),
        ('mid_level', 'Mid Level'),
        ('senior_level', 'Senior Level'),
        ('executive', 'Executive'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('closed', 'Closed'),
        ('expired', 'Expired'),
    ]
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    
    # Let's define as Location and Remote
    location = models.CharField(max_length=255, blank=True)
    is_remote = models.BooleanField(default=False)
    remote_type = models.CharField(
        max_length=20,
        choices=[
            ('fully_remote', 'Fully Remote'),
            ('hybrid', 'Hybrid'),
            ('on_site', 'On Site')
        ],
        default='on_site'
    )
    
    # Job Details
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, default='full_time')
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES, default='mid_level')
    
    # Salary Information
    salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=3, default='USD')
    salary_type = models.CharField(
        max_length=20,
        choices=[
            ('hourly', 'Hourly'),
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly')
        ],
        default='yearly'
    )
    show_salary = models.BooleanField(default=True)
    
    # Status and Visibility
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_urgent = models.BooleanField(default=False)
    
    # Application
    application_url = models.URLField(blank=True, help_text="External application URL")
    application_email = models.EmailField(blank=True)
    accept_applications = models.BooleanField(default=True)
    
    # Skills (stored as comma-separated values for simplicity)
    skills_required = models.TextField(blank=True, help_text="Comma-separated list of skills")
    
    # Dates
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relationships
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='jobs')
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posted_jobs')
    
    # Statistics
    views_count = models.PositiveIntegerField(default=0)
    applications_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'jobs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', 'status']),
            models.Index(fields=['location']),
            models.Index(fields=['job_type']),
            models.Index(fields=['experience_level']),
            models.Index(fields=['created_at']),
            models.Index(fields=['expires_at']),
        ]
    
    def __str__(self):
        return f"{self.title} at {self.company.name}"
    
    @property
    def is_expired(self):
        return timezone.now() > self.expires_at if self.expires_at else False
    
    @property
    def skills_list(self):
        if self.skills_required:
            return [skill.strip() for skill in self.skills_required.split(',')]
        return []
    
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])