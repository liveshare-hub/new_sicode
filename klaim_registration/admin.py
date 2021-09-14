from django.contrib import admin

from .models import DataKlaim, ApprovalHRD, toQRCode, DataTK, NoKPJ, SebabKlaim

admin.site.register(SebabKlaim)
admin.site.register(DataKlaim)
admin.site.register(DataTK)
admin.site.register(ApprovalHRD)
admin.site.register(toQRCode)
admin.site.register(NoKPJ)
