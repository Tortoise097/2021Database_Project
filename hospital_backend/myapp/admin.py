from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Patient, Doctor, Appointment, MedicalRecord, Prescription

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(MedicalRecord)
admin.site.register(Prescription)