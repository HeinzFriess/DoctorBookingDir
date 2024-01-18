from django.contrib import admin
from django.contrib.auth.models import User
from .models import Doctor, Patient, Appointment

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('title', 'first_name', 'last_name', 'speciality', 'id') 
    
    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    first_name.short_description = 'First Name'
    last_name.short_description = 'Last Name'

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'id')
    
    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    first_name.short_description = 'First Name'
    last_name.short_description = 'Last Name'

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'doctor', 'patient', 'created_at')

