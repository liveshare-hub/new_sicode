# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import create_user, login_view, register_user, register_user_ajax, settingProfile, DetilProfile, DetilProfileTK, ListPerusahaan
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path('register/ajax', create_user, name="create-user"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", DetilProfile, name="profile"),
    path("profile/tk/<int:pk>/", DetilProfileTK, name="profile-tk"),
    path("profile/edit/<int:pk>/", settingProfile, name="update_profile"),
    path("api/perusahaan/", ListPerusahaan.as_view(), name="api-perusahaan"),
]
