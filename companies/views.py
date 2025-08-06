from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from django.db.models import Count
from .models import Company
from .serializers import (
    CompanyListSerializer, CompanyDetailSerializer, CompanyCreateUpdateSerializer
)
from django.db.models import Count, Q


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
        description="Create a new company (Admin only)"
    )
)
class CompanyCreateView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Only admins and employers can create companies
        if self.request.user.role not in ['admin', 'employer']:
            raise permissions.PermissionDenied("Only admins and employers can create companies")
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
        description="Update company information (Admin only)"
    ),
    patch=extend_schema(
        summary="Partially update company",
        description="Partially update company information (Admin only)"
    ),
    delete=extend_schema(
        summary="Delete company",
        description="Delete a company (Admin only)"
    )
)
class CompanyUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated] # Ensure the user is authenticated
    lookup_field = 'slug'

    def perform_update(self, serializer):
        # self.request.user should have a 'role' attribute (from your authentication setup)
        if self.request.user.role != 'employer':
            raise PermissionDenied("Only admins can update companies") # <--- Use the imported PermissionDenied
        serializer.save()

    def perform_destroy(self, instance):
        # self.request.user should have a 'role' attribute
        if self.request.user.role != 'admin':
            raise PermissionDenied("Only admins can delete companies") # <--- Use the imported PermissionDenied
        instance.delete()