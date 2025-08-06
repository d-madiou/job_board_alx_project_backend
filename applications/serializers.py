# applications/serializers.py
from rest_framework import serializers
from django.utils import timezone
from authentication.serializers import UserProfileSerializer
from jobs.serializers import JobListSerializer
from .models import Application

class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'job', 'cover_letter', 'resume_url', 'portfolio_url',
            'linkedin_url', 'phone', 'email', 'years_of_experience',
            'expected_salary', 'availability_date'
        ]
    
    def validate_job(self, value):
        # Check if job is still accepting applications
        if not value.accept_applications:
            raise serializers.ValidationError("This job is no longer accepting applications.")
        
        if not value.is_active or value.status != 'active':
            raise serializers.ValidationError("This job is not currently active.")
        
        if value.is_expired:
            raise serializers.ValidationError("This job posting has expired.")
        
        # Check if user already applied
        user = self.context['request'].user
        if Application.objects.filter(job=value, applicant=user).exists():
            raise serializers.ValidationError("You have already applied for this job.")
        
        return value
    
    def create(self, validated_data):
        validated_data['applicant'] = self.context['request'].user
        return super().create(validated_data)

class ApplicationListSerializer(serializers.ModelSerializer):
    job = JobListSerializer(read_only=True)
    applicant_name = serializers.CharField(source='applicant.get_full_name', read_only=True)
    applicant_email = serializers.CharField(source='applicant.email', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'job', 'applicant_name', 'applicant_email', 'status',
            'years_of_experience', 'expected_salary', 'applied_at', 'updated_at'
        ]

class ApplicationDetailSerializer(serializers.ModelSerializer):
    job = JobListSerializer(read_only=True)
    applicant = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'job', 'applicant', 'cover_letter', 'resume_url',
            'portfolio_url', 'linkedin_url', 'phone', 'email',
            'status', 'admin_notes', 'rejection_reason',
            'years_of_experience', 'expected_salary', 'availability_date',
            'applied_at', 'updated_at', 'reviewed_at'
        ]

class ApplicationUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status', 'admin_notes', 'rejection_reason']
    
    def update(self, instance, validated_data):
        # Set reviewed_at timestamp when status changes
        if 'status' in validated_data and validated_data['status'] != instance.status:
            validated_data['reviewed_at'] = timezone.now()
        
        return super().update(instance, validated_data)

class MyApplicationSerializer(serializers.ModelSerializer):
    job = JobListSerializer(read_only=True)
    company_name = serializers.CharField(source='job.company.name', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'job', 'company_name', 'cover_letter', 'resume_url',
            'portfolio_url', 'linkedin_url', 'status', 'rejection_reason',
            'years_of_experience', 'expected_salary', 'availability_date',
            'applied_at', 'updated_at'
        ]