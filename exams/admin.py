from django.contrib import admin
from .models import ExamsTypes, ExamRequest, ExamsOrders, MedicalAccess

# Register your models here.
admin.site.register(ExamsTypes)
admin.site.register(ExamRequest)
admin.site.register(ExamsOrders)
admin.site.register(MedicalAccess)