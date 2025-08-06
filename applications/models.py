# applications/models.py
from django.db import models
from django.contrib.auth import get_user_model
from jobs.models import Job

User = get_user_model()

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('interviewed', 'Interviewed'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    
    # Application content
    cover_letter = models.TextField(blank=True, help_text="Cover letter content")
    resume_url = models.URLField(blank=True, help_text="URL to resume file")
    portfolio_url = models.URLField(blank=True, help_text="Portfolio website URL")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn profile URL")
    
    # Contact information (in case it differs from user profile)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    
    # Application status and notes
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, help_text="Internal notes from HR/Admin")
    rejection_reason = models.TextField(blank=True)
    
    # Timestamps
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Additional fields
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    expected_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    availability_date = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'applications'
        unique_together = ['job', 'applicant']  # Prevent duplicate applications
        ordering = ['-applied_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['applied_at']),
            models.Index(fields=['job', 'status']),
        ]
    
    def __str__(self):
        return f"{self.applicant.get_full_name()} applied for {self.job.title}"
    
    def save(self, *args, **kwargs):
        # Update job's application count
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            self.job.applications_count = self.job.applications.count()
            self.job.save(update_fields=['applications_count'])
    
    def delete(self, *args, **kwargs):
        job = self.job
        super().delete(*args, **kwargs)
        # Update job's application count after deletion
        job.applications_count = job.applications.count()
        job.save(update_fields=['applications_count'])