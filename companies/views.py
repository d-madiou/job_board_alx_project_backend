# companies/views.py - Updated views to handle file uploads
from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from django.db.models import Count, Q
from .models import Company
from .serializers import (
    CompanyListSerializer, CompanyDetailSerializer, CompanyCreateUpdateSerializer
)

@extend_schema_view(
    get=extend_schema(
        summary="List all companies",
        description="Get a paginated list of all companies with filtering options",
        parameters=[
            OpenApiParameter(name='search', description='Search in company name and description'),
            OpenApiParameter(name='location', description='Filter by company location'),
            OpenApiParameter(name='industry', description='Filter by company industry'),
            OpenApiParameter(name='size', description='Filter by company size'),
            OpenApiParameter(name='is_verified', description='Filter by verification status'),
        ]
    )
)
class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.annotate(
        active_job_count=Count('jobs', filter=Q(jobs__is_active=True))
    )
    serializer_class = CompanyListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location', 'industry', 'size', 'is_verified']
    search_fields = ['name', 'description', 'industry']
    ordering_fields = ['name', 'created_at', 'active_job_count']
    ordering = ['name']

@extend_schema_view(
    post=extend_schema(
        summary="Create a new company",
        description="Create a new company with logo upload (Admin/Employer only)"
    )
)
class CompanyCreateView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # Add parsers for file uploads

    def perform_create(self, serializer):
        # Only admins and employers can create companies
        if self.request.user.role not in ['admin', 'employer']:
            raise PermissionDenied("Only admins and employers can create companies")
        serializer.save()

@extend_schema_view(
    get=extend_schema(
        summary="Get company details",
        description="Retrieve detailed information about a specific company"
    )
)
class CompanyDetailView(generics.RetrieveAPIView):
    queryset = Company.objects.annotate(
         active_job_count=Count('jobs', filter=Q(jobs__is_active=True))
    )
    serializer_class = CompanyDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

@extend_schema_view(
    put=extend_schema(
        summary="Update company",
        description="Update company information with logo upload (Employer only)"
    ),
    patch=extend_schema(
        summary="Partially update company",
        description="Partially update company information with logo upload (Employer only)"
    ),
    delete=extend_schema(
        summary="Delete company",
        description="Delete a company (Admin only)"
    )
)
class CompanyUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # Add parsers for file uploads
    lookup_field = 'slug'

    def perform_update(self, serializer):
        if self.request.user.role != 'employer':
            raise PermissionDenied("Only employers can update companies")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role != 'admin':
            raise PermissionDenied("Only admins can delete companies")
        instance.delete()