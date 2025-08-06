# companies/serializers.py
from rest_framework import serializers
from django.utils.text import slugify
from .models import Company

class CompanyListSerializer(serializers.ModelSerializer):
    job_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'slug', 'description', 'logo_url', 'location',
            'size', 'industry', 'is_verified', 'job_count', 'created_at'
        ]

class CompanyDetailSerializer(serializers.ModelSerializer):
    job_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'slug', 'description', 'website', 'logo_url',
            'location', 'size', 'founded_year', 'industry', 'is_verified',
            'email', 'phone', 'linkedin_url', 'twitter_url', 'facebook_url',
            'job_count', 'created_at', 'updated_at'
        ]

class CompanyCreateUpdateSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    
    class Meta:
        model = Company
        fields = [
            'name', 'slug', 'description', 'website', 'logo_url', 'location',
            'size', 'founded_year', 'industry', 'email', 'phone',
            'linkedin_url', 'twitter_url', 'facebook_url'
        ]
    
    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['slug'] = slugify(validated_data['name'])
        return super().update(instance, validated_data)