# jobs/views.py
from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from django.db.models import Q, F
from django.utils import timezone
from .models import Job, Category
from .serializers import (
    JobListSerializer, JobDetailSerializer, JobCreateUpdateSerializer,
    CategorySerializer, CategoryCreateUpdateSerializer
)
from .filters import JobFilter

@extend_schema_view(
    get=extend_schema(
        summary="List all categories",
        description="Get a list of all job categories"
    )
)
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

@extend_schema_view(
    post=extend_schema(
        summary="Create a new category",
        description="Create a new job category (Admin only)"
    )
)
class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        if self.request.user.role != 'admin':
            raise permissions.PermissionDenied("Only admins can create categories")
        serializer.save()

# Job Views
@extend_schema_view(
    get=extend_schema(
        summary="List all jobs",
        description="Get a paginated list of all active jobs with filtering options",
        parameters=[
            OpenApiParameter(name='search', description='Search in job title and description'),
            OpenApiParameter(name='location', description='Filter by job location'),
            OpenApiParameter(name='job_type', description='Filter by job type'),
            OpenApiParameter(name='experience_level', description='Filter by experience level'),
            OpenApiParameter(name='category', description='Filter by category ID'),
            OpenApiParameter(name='company', description='Filter by company ID'),
            OpenApiParameter(name='is_remote', description='Filter remote jobs'),
            OpenApiParameter(name='salary_min', description='Minimum salary filter'),
            OpenApiParameter(name='salary_max', description='Maximum salary filter'),
        ]
    )
)
class JobListView(generics.ListAPIView):
    serializer_class = JobListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'description', 'company__name', 'skills_required']
    ordering_fields = ['created_at', 'title', 'salary_min', 'views_count', 'applications_count']
    ordering = ['-is_featured', '-is_urgent', '-created_at']
    
    def get_queryset(self):
        return Job.objects.filter(
            is_active=True, 
            status='active'
        ).select_related('company', 'category', 'posted_by')

@extend_schema_view(
    post=extend_schema(
        summary="Create a new job",
        description="Create a new job posting (Admin and Employer only)"
    )
)
class JobCreateView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        if self.request.user.role not in ['admin', 'employer']:
            raise permissions.PermissionDenied("Only admins and employers can create jobs")
        serializer.save()

@extend_schema_view(
    get=extend_schema(
        summary="Get job details",
        description="Retrieve detailed information about a specific job"
    )
)
class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.select_related('company', 'category', 'posted_by')
    serializer_class = JobDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increment_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

@extend_schema_view(
    put=extend_schema(
        summary="Update job",
        description="Update job information (Admin and job owner only)"
    ),
    patch=extend_schema(
        summary="Partially update job",
        description="Partially update job information (Admin and job owner only)"
    ),
    delete=extend_schema(
        summary="Delete job",
        description="Delete a job (Admin and job owner only)"
    )
)
class JobUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'
    
    def perform_update(self, serializer):
        job = self.get_object()
        user = self.request.user
        
        if user.role != 'admin' and job.posted_by != user:
            raise permissions.PermissionDenied("You can only update your own job postings")
        
        serializer.save()
    
    def perform_destroy(self, instance):
        user = self.request.user
        
        if user.role != 'admin' and instance.posted_by != user:
            raise permissions.PermissionDenied("You can only delete your own job postings")
        
        instance.delete()

@extend_schema(
    summary="Get featured jobs",
    description="Get a list of featured job postings"
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_jobs_view(request):
    jobs = Job.objects.filter(
        is_active=True, 
        status='active', 
        is_featured=True
    ).select_related('company', 'category')[:10]
    
    serializer = JobListSerializer(jobs, many=True)
    return Response(serializer.data)

@extend_schema(
    summary="Get recent jobs",
    description="Get recently posted jobs"
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def recent_jobs_view(request):
    jobs = Job.objects.filter(
        is_active=True, 
        status='active'
    ).select_related('company', 'category').order_by('-created_at')[:10]
    
    serializer = JobListSerializer(jobs, many=True)
    return Response(serializer.data)

@extend_schema(
    summary="Get job statistics",
    description="Get overall job board statistics"
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def job_stats_view(request):
    from companies.models import Company
    
    stats = {
        'total_jobs': Job.objects.filter(is_active=True, status='active').count(),
        'total_companies': Company.objects.filter(is_verified=True).count(),
        'total_categories': Category.objects.filter(is_active=True).count(),
        'featured_jobs': Job.objects.filter(is_active=True, status='active', is_featured=True).count(),
        'remote_jobs': Job.objects.filter(is_active=True, status='active', is_remote=True).count(),
    }
    
    return Response(stats)