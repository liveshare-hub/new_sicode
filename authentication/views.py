# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib import messages
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from .forms import LoginForm, SignUpForm, ProfileForm

from klaim_registration.form import DataTK
from .models import Profile


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


def register_user(request):

    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password1 = form.cleaned_data.get("password1")
            raw_password2 = form.cleaned_data.get("password2")
            if raw_password1 != raw_password2:
                msg = 'Password tidak sama'
            else:
                user = authenticate(username=username, password=raw_password1)

                msg = 'User created - please <a href="/login">login</a>.'
                success = True

                return redirect("register")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


def DetilProfile(request):
    qs = Profile.objects.select_related(
        'user').filter(user__username=request.user)
    context = {
        'datas': qs
    }
    return render(request, 'authentication/profile.html', context)


def DetilProfileTK(request, pk):
    qs = Profile.objects.select_related('user').filter(pk=pk)
    context = {
        'datas': qs
    }
    return render(request, 'authentication/profile.html', context)


def settingProfile(request, pk):
    qs = get_object_or_404(Profile, pk=pk)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,
                           instance=qs)
        if form.is_valid():

            post = form.save(commit=False)
            post.npp = form.cleaned_data['npp']
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


# def registerHRD(request):
#     if request.method == 'POST':
#         form = DaftarHRDForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             username = post.npp.npp
#             password = make_password('WELCOME1', salt=['username'])
#             buat_user = User.objects.create(
#                 username=username, password=password)
#             post.user__username = buat_user.username
#             print(buat_user.id)
#             group = Group.objects.get(name='hrd')
#             buat_user.groups.add(group)
#             post.save()
#             messages.SUCCESS(request, 'Akun '+username+' berhasil dibuat')
#             return redirect('login')
#     else:
#         form = DaftarHRDForm()
#     return render(request, "accounts/register.html", {'form': form})
