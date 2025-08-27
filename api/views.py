"""
Healthcare API Views

This module contains the view classes for the Healthcare API.
It includes views for user authentication, patient management,
doctor management, and patient-doctor relationships.
"""

from typing import Any, Dict, List, Optional
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    UserSerializer,
    PatientSerializer,
    DoctorSerializer,
    PatientDoctorMappingSerializer
)


class RegisterView(generics.CreateAPIView):
    """
    API View for user registration.
    Allows new users to create an account.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user management.
    Provides CRUD operations for user accounts.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self) -> QuerySet:
        """
        Override to ensure users can only access their own data.
        """
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)


class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing patient records.
    Provides CRUD operations for patient data.
    """
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        """
        Returns queryset of patients belonging to the authenticated user.
        """
        return Patient.objects.filter(user=self.request.user)

    def perform_create(self, serializer: PatientSerializer) -> None:
        """
        Associates the patient with the authenticated user during creation.
        
        Args:
            serializer: The patient serializer instance
        """
        serializer.save(user=self.request.user)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Custom update method to ensure users can only update their own patients.
        
        Args:
            request: The HTTP request
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            Response: The HTTP response
        """
        patient = self.get_object()
        if patient.user != request.user:
            return Response(
                {'error': 'You do not have permission to update this patient.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)


class DoctorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing doctor records.
    Provides CRUD operations for doctor data.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer: DoctorSerializer) -> None:
        """
        Additional validation before creating a doctor.
        
        Args:
            serializer: The doctor serializer instance
        """
        try:
            serializer.save()
        except ValidationError as e:
            raise ValidationError({'error': str(e)})


class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing patient-doctor relationships.
    Handles the mapping between patients and their assigned doctors.
    """
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        """
        Returns filtered queryset based on patient_id if provided in query parameters.
        
        Returns:
            QuerySet: Filtered patient-doctor mappings
        """
        base_queryset = PatientDoctorMapping.objects.select_related('patient', 'doctor')
        patient_id = self.request.query_params.get('patient_id')
        
        if patient_id:
            return base_queryset.filter(
                patient_id=patient_id,
                patient__user=self.request.user
            )
        return base_queryset.filter(patient__user=self.request.user)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Creates a new patient-doctor mapping with validation.
        
        Args:
            request: The HTTP request
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            Response: The HTTP response
        """
        patient_id = request.data.get('patient')
        doctor_id = request.data.get('doctor')

        # Validate patient ownership
        patient = get_object_or_404(Patient, id=patient_id)
        if patient.user != request.user:
            return Response(
                {'error': 'You do not have permission to assign this patient.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Validate doctor exists
        get_object_or_404(Doctor, id=doctor_id)

        # Check for existing mapping
        if PatientDoctorMapping.objects.filter(
            patient_id=patient_id,
            doctor_id=doctor_id
        ).exists():
            return Response(
                {'error': 'This patient is already assigned to this doctor.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Removes a patient-doctor mapping with ownership validation.
        
        Args:
            request: The HTTP request
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            Response: The HTTP response
        """
        mapping = self.get_object()
        if mapping.patient.user != request.user:
            return Response(
                {'error': 'You do not have permission to remove this mapping.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
