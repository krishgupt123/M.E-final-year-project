from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Patient_info,UserPredictModel

admin.site.register(Patient_info)
admin.site.register(UserPredictModel)

from .models import PatientRecord

admin.site.register(PatientRecord)