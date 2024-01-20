from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Patient, Doctor, Appointment
from .serializers import PatientSerializer, DoctorSerializer, AppointmentSerializer, UserSerializer
from django.contrib.auth.models import User

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
    def create(self, request, *args, **kwargs):
        user_data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email': request.data.get('email'),
        }

        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = User.objects.create_user(**user_serializer.validated_data)
            request.data['user'] = user.id
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        user = instance.user
        user.delete()

        self.perform_destroy(instance)

        return Response({"detail": "Patient successfully deleted."}, status=status.HTTP_204_NO_CONTENT)

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def create(self, request, *args, **kwargs):
        user_data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email': request.data.get('email'),
        }

        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = User.objects.create_user(**user_serializer.validated_data)
            request.data['user'] = user.id
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        user = instance.user
        user.delete()

        self.perform_destroy(instance)

        return Response({"detail": "Doctor successfully deleted."}, status=status.HTTP_204_NO_CONTENT)

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if hasattr(user, 'patient'):
                return Appointment.objects.filter(patient=user.patient)
            elif hasattr(user, 'doctor'):
                return Appointment.objects.filter(doctor=user.doctor)
        return Appointment.objects.none()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Appointment successfully deleted."}, status=status.HTTP_204_NO_CONTENT)