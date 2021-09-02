from django.contrib import admin

from .models import DataKlaim, ApprovalHRD, toQRCode, DataTK, NoKPJ

admin.site.register(DataKlaim)
admin.site.register(DataTK)
admin.site.register(ApprovalHRD)
admin.site.register(toQRCode)
admin.site.register(NoKPJ)
