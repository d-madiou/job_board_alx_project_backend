# jobs/serializers.py
from rest_framework import serializers
from django.utils.text import slugify
from companies.serializers import CompanyListSerializer
from .models import Job, Category

class CategorySerializer(serializers.ModelSerializer):
    job_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'job_count']

class JobListSerializer(serializers.ModelSerializer):
    company = CompanyListSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    skills_list = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'slug', 'company', 'category', 'location', 
            'is_remote', 'remote_type', 'job_type', 'experience_level',
            'salary_min', 'salary_max', 'salary_currency', 'salary_type', 'show_salary',
            'is_featured', 'is_urgent', 'skills_list', 'views_count',
            'applications_count', 'created_at', 'expires_at', 'is_expired'
        ]

class JobDetailSerializer(serializers.ModelSerializer):
    company = CompanyListSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    skills_list = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    posted_by_name = serializers.CharField(source='posted_by.full_name', read_only=True)
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'slug', 'description', 'requirements', 
            'responsibilities', 'benefits', 'company', 'category',
            'location', 'is_remote', 'remote_type', 'job_type', 'experience_level',
            'salary_min', 'salary_max', 'salary_currency', 'salary_type', 'show_salary',
            'status', 'is_featured', 'is_urgent', 'application_url', 'application_email',
            'accept_applications', 'skills_list', 'views_count', 'applications_count',
            'posted_by_name', 'created_at', 'updated_at', 'expires_at', 'is_expired'
        ]

class JobCreateUpdateSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    
    class Meta:
        model = Job
        fields = [
            'title', 'slug', 'description', 'requirements', 'responsibilities', 'benefits',
            'company', 'category', 'location', 'is_remote', 'remote_type',
            'job_type', 'experience_level', 'salary_min', 'salary_max',
            'salary_currency', 'salary_type', 'show_salary', 'status',
            'is_featured', 'is_urgent', 'application_url', 'application_email',
            'accept_applications', 'skills_required', 'expires_at'
        ]
    
    def create(self, validated_data):
        # Generate slug from title
        validated_data['slug'] = slugify(validated_data['title'])
        validated_data['posted_by'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Update slug if title changes
        if 'title' in validated_data:
            validated_data['slug'] = slugify(validated_data['title'])
        return super().update(instance, validated_data)

class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    
    class Meta:
        model = Category
        fields = ['name', 'slug','description', 'icon', 'is_active']
    
    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['slug'] = slugify(validated_data['name'])
        return super().update(instance, validated_data)