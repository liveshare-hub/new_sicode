# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
# from django_filters import filters
from django.http import response
from django.http.response import JsonResponse
from authentication.serializer import PerusahaanSerializer
from django.contrib import messages
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from rest_framework.generics import ListCreateAPIView
from rest_framework.utils import serializer_helpers
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from .forms import LoginForm, SignUpForm, ProfileForm

from klaim_registration.form import DataTK, NoKPJ
from .models import Profile, Perusahaan

from .filter import PerusahaanFilter, PerusahaanList


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


# def register_user(request):

#     msg = None
#     success = False

#     companies = Perusahaan.objects.all()
#     myFilter = PerusahaanFilter(request.GET, queryset=companies)
#     qs = myFilter.qs

#     if request.method == "POST":

#         form = SignUpForm(request.POST)
#         if form.is_valid():

#             form.save()
#             username = form.cleaned_data.get("username")
#             raw_password1 = form.cleaned_data.get("password1")
#             raw_password2 = form.cleaned_data.get("password2")
#             # npp = request.POST.get("no_npp")

#             if raw_password1 != raw_password2:
#                 msg = 'Password tidak sama'
#             else:
#                 user = authenticate(username=username, password=raw_password1)
#                 try:
#                     Profile.objects.update_or_create(user__username=user, defaults={
#                                                      'npp_id': npp, 'nama': 'BELUM UPDATE'},)
#                 except:
#                     return redirect("register")

#                 msg = 'User created - please <a href="/login">login</a>.'
#                 success = True

#                 return redirect("register")

#         else:
#             msg = 'Form is not valid'
#     else:
#         form = SignUpForm()

#     return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success, "qs": qs, "myFilter": myFilter})

def register_user(request):

    return render(request, 'accounts/register.html')


def register_user_ajax(request):
    msg = None
    if request.is_ajax():
        username = request.POST.get('username', None)
        password1 = request.POST.get('password1', None)
        password2 = request.POST.get('password2', None)
        npp_id = request.POST.get('no_npp')
        if (password1 != password2):
            msg = 'Password tidak sama'
        else:
            user = authenticate(username=username, password=password1)
            try:
                Profile.objects.update_or_create(
                    user__username=username, defaults={'npp_id': npp_id})
            except:
                return redirect('register')
            msg = 'User created - please <a href="/login">login'
            response = {
                'msg': msg
            }
            return JsonResponse(response)


def create_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        npp_id = request.POST['no_npp']

        if password1 != password2:
            msg = 'Password Tidak Sama!'
        else:
            password = make_password(password1, salt=['username'])
            User.objects.create(username=username, password=password)
            try:
                Profile.objects.update_or_create(
                    user__username=username, defaults={'npp_id': npp_id})
            except:
                pass
            msg = 'User Created - Please <a href="/accounts/login">login</a>'
            response = {
                'msg': msg
            }
            return JsonResponse(response)


def DetilProfile(request):
    qs = Profile.objects.select_related(
        'user').filter(user__username=request.user)
    context = {
        'datas': qs
    }
    return render(request, 'authentication/profile.html', context)


def DetilProfileTK(request, pk):
    qs = Profile.objects.select_related('user').filter(pk=pk)
    datas_na = NoKPJ.objects.select_related('user_kpj').filter(
        user_kpj__npp_id=request.user.profile.npp_id, user_kpj_id=pk)
    context = {
        'datas': qs,
        'datas_na': datas_na
    }
    return render(request, 'authentication/profile_tk.html', context)


def settingProfile(request, pk):
    qs = get_object_or_404(Profile, pk=pk)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,
                           instance=qs)
        if form.is_valid():

            post = form.save(commit=False)
            # post.npp = form.cleaned_data['npp']
            post.nama = form.cleaned_data['nama']
            post.tgl_lahir = form.cleaned_data['tgl_lahir']
            post.tempat_lahir = form.cleaned_data['tempat_lahir']
            post.nik = form.cleaned_data['nik']
            post.no_hp = form.cleaned_data['no_hp']
            post.is_hrd = form.cleaned_data['is_hrd']
            # DataTK.objects.select_related('profile').create(
            #     profile_id=request.user.profile.id)
            post.save()

            return redirect('list-kpj')
    else:
        form = ProfileForm(instance=qs)

    return render(request, "authentication/update_form.html", {'form': form, 'qs': qs})


class ListPerusahaan(ListCreateAPIView):
    serializer_class = PerusahaanSerializer
    permission_classes = [permissions.AllowAny, ]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['npp', ]
    search_fields = ['npp', ]

    # def get(self, request, format=None):

    #     companies = [comp.nama for comp in Perusahaan.objects.all()]
    #     return Response(companies)

    def get_queryset(self):

        qs = Perusahaan.objects.all()
        if qs.exists():
            return qs
        else:
            return qs.none
