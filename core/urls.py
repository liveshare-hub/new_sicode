# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path("klaim/", include("klaim_registration.urls")),
    path('admin/', admin.site.urls),          # Django admin route
    path('admin', admin.site.urls),          # Django admin route
    # path('qr_code/', include('qr_code.urls', namespace="qr_code")),
    # Auth routes - login / register
    path('accounts/', include("authentication.urls")),
    path("", include("app.urls"))             # UI Kits Html files
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# SERVE_QR_CODE_IMAGE_PATH = 'media/qr-code-image/'
