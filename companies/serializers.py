# companies/serializers.py
from rest_framework import serializers
from django.utils.text import slugify
from .models import Company

class CompanyListSerializer(serializers.ModelSerializer):
    job_count = serializers.ReadOnlyField()
    logo_display_url = serializers.ReadOnlyField()
    
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'slug', 'description', 'logo_display_url', 'location',
            'size', 'industry', 'is_verified', 'job_count', 'created_at'
        ]

class CompanyDetailSerializer(serializers.ModelSerializer):
    job_count = serializers.ReadOnlyField()
    logo_display_url = serializers.ReadOnlyField()
    
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'slug', 'description', 'website', 'logo_display_url',
            'location', 'size', 'founded_year', 'industry', 'is_verified',
            'email', 'phone', 'linkedin_url', 'twitter_url', 'facebook_url',
            'job_count', 'created_at', 'updated_at'
        ]

class CompanyCreateUpdateSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    logo = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = Company
        fields = [
            'name', 'slug', 'description', 'website', 'logo', 'logo_url', 'location',
            'size', 'founded_year', 'industry', 'email', 'phone',
            'linkedin_url', 'twitter_url', 'facebook_url'
        ]
    
    def validate_logo(self, value):
        """Validate logo file"""
        if value:
            # Check file size (limit to 5MB)
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("Logo file too large. Maximum size is 5MB.")
            
            # Check file format
            allowed_formats = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if value.content_type not in allowed_formats:
                raise serializers.ValidationError(
                    "Invalid file format. Allowed formats: JPEG, PNG, GIF, WebP."
                )
        
        return value
    
    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['slug'] = slugify(validated_data['name'])
        
        # Handle logo file replacement
        if 'logo' in validated_data and validated_data['logo']:
            # Delete old logo file if exists
            if instance.logo:
                instance.logo.delete(save=False)
        
        return super().update(instance, validated_data)