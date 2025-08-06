# applications/views.py
from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from django.db.models import Q
from .models import Application
from .serializers import (
    ApplicationCreateSerializer, ApplicationListSerializer,
    ApplicationDetailSerializer, ApplicationUpdateStatusSerializer,
    MyApplicationSerializer
)

@extend_schema_view(
    post=extend_schema(
        summary="Apply for a job",
        description="Submit an application for a job posting"
    )
)
class ApplicationCreateView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        if self.request.user.role not in ['user', 'admin']:
            raise permissions.PermissionDenied("Only job seekers can apply for jobs")
        serializer.save()

@extend_schema_view(
    get=extend_schema(
        summary="List job applications",
        description="Get applications for jobs posted by the authenticated user (Employers/Admins only)",
        parameters=[
            OpenApiParameter(name='job', description='Filter by job ID'),
            OpenApiParameter(name='status', description='Filter by application status'),
            OpenApiParameter(name='search', description='Search in applicant name and email'),
        ]
    )
)
class ApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'job']
    search_fields = ['applicant__first_name', 'applicant__last_name', 'applicant__email']
    ordering_fields = ['applied_at', 'updated_at', 'status']
    ordering = ['-applied_at']
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'admin':
            # Admins can see all applications
            return Application.objects.select_related('job', 'applicant')
        elif user.role == 'employer':
            # Employers can see applications for their jobs
            return Application.objects.filter(
                job__posted_by=user
            ).select_related('job', 'applicant')
        else:
            # Regular users shouldn't access this endpoint
            return Application.objects.none()

@extend_schema_view(
    get=extend_schema(
        summary="Get application details",
        description="Retrieve detailed information about a specific application"
    )
)
class ApplicationDetailView(generics.RetrieveAPIView):
    serializer_class = ApplicationDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'admin':
            return Application.objects.select_related('job', 'applicant')
        elif user.role == 'employer':
            return Application.objects.filter(
                job__posted_by=user
            ).select_related('job', 'applicant')
        else:
            # Users can only see their own applications
            return Application.objects.filter(
                applicant=user
            ).select_related('job', 'applicant')

@extend_schema_view(
    patch=extend_schema(
        summary="Update application status",
        description="Update the status of an application (Employers/Admins only)"
    )
)
class ApplicationUpdateView(generics.UpdateAPIView):
    serializer_class = ApplicationUpdateStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'admin':
            return Application.objects.all()
        elif user.role == 'employer':
            return Application.objects.filter(job__posted_by=user)
        else:
            return Application.objects.none()
    
    def perform_update(self, serializer):
        if self.request.user.role not in ['admin', 'employer']:
            raise permissions.PermissionDenied("Only employers and admins can update application status")
        serializer.save()

@extend_schema_view(
    get=extend_schema(
        summary="Get my applications",
        description="Get all applications submitted by the authenticated user"
    )
)
class MyApplicationsView(generics.ListAPIView):
    serializer_class = MyApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['status']
    ordering_fields = ['applied_at', 'updated_at']
    ordering = ['-applied_at']
    
    def get_queryset(self):
        return Application.objects.filter(
            applicant=self.request.user
        ).select_related('job', 'job__company')

@extend_schema(
    summary="Withdraw application",
    description="Withdraw a job application"
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def withdraw_application_view(request, application_id):
    try:
        application = Application.objects.get(
            id=application_id,
            applicant=request.user
        )
        
        if application.status in ['accepted', 'rejected']:
            return Response(
                {'error': 'Cannot withdraw an application that has been accepted or rejected'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.status = 'withdrawn'
        application.save()
        
        return Response(
            {'message': 'Application withdrawn successfully'},
            status=status.HTTP_200_OK
        )
        
    except Application.DoesNotExist:
        return Response(
            {'error': 'Application not found'},
            status=status.HTTP_404_NOT_FOUND
        )

@extend_schema(
    summary="Get application statistics",
    description="Get application statistics for the authenticated user's jobs"
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def application_stats_view(request):
    user = request.user
    
    if user.role == 'admin':
        queryset = Application.objects.all()
    elif user.role == 'employer':
        queryset = Application.objects.filter(job__posted_by=user)
    else:
        # For job seekers, show their application stats
        queryset = Application.objects.filter(applicant=user)
        stats = {
            'total_applications': queryset.count(),
            'pending': queryset.filter(status='pending').count(),
            'reviewed': queryset.filter(status='reviewed').count(),
            'shortlisted': queryset.filter(status='shortlisted').count(),
            'interviewed': queryset.filter(status='interviewed').count(),
            'accepted': queryset.filter(status='accepted').count(),
            'rejected': queryset.filter(status='rejected').count(),
            'withdrawn': queryset.filter(status='withdrawn').count(),
        }
        return Response(stats)
    
    # For admins and employers
    stats = {
        'total_applications': queryset.count(),
        'pending': queryset.filter(status='pending').count(),
        'reviewed': queryset.filter(status='reviewed').count(),
        'shortlisted': queryset.filter(status='shortlisted').count(),
        'interviewed': queryset.filter(status='interviewed').count(),
        'accepted': queryset.filter(status='accepted').count(),
        'rejected': queryset.filter(status='rejected').count(),
        'withdrawn': queryset.filter(status='withdrawn').count(),
    }
    
    return Response(stats)