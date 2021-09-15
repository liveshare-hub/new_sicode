# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Perusahaan


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    # npp = forms.ModelChoiceField(required=False, queryset=Perusahaan.objects.all(), widget=forms.Select(attrs={
    #     'class': 'form-control'
    # }))

    class Meta:
        model = Profile
        fields = ('propic', 'nama', 'tgl_lahir',
                  'tempat_lahir', 'nik', 'no_hp', 'is_hrd',)
        exclude = ('user', 'npp',)

        widgets = {
            'propic': forms.FileInput(attrs={
                'class': 'from-control'
            }),

            'nama': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nama Lengkap'
            }),
            'tgl_lahir': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
            'tempat_lahir': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Tempat Lahir'
            }),
            'nik': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'No KTP'
            }),
            'no_hp': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'No. Handphone'
            }),
            'is_hrd': forms.Select(attrs={
                'class': 'form-control'
            })
        }
