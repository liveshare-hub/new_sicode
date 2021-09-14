from django import forms
from django.db import models
from django.forms import widgets
from datetime import datetime
# from dal import autocomplete

from .models import DataKlaim, DataTK, NoKPJ, SebabKlaim


STATUS = (
    ('1', 'BELUM MENIKAH'),
    ('2', 'MENIKAH')
)


class DataKlaimForm(forms.ModelForm):
    file_lain = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
            }
        ))

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan Email Anda'
        })
    )

    sebab_klaim = forms.ModelChoiceField(
        queryset=SebabKlaim.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = DataKlaim
        exclude = ('data_tk',)
        widgets = {
            'tipe_klaim': forms.Select(attrs={
                'class': 'form-control'
            }),
            'nama_rekening': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'NAMA PEMILIK REKENING'
            }),
            'no_rekening': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'NO REKENING'
            }),
            'file_kk': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'file_ktp': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'file_paklaring': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }


class DataTKForm(forms.ModelForm):
    kpj = forms.ModelChoiceField(
        required=False, queryset=NoKPJ.objects.all(), widget=forms.Select(attrs={
            'class': 'form-control data-select'
        }))

    # def __init__(self, *args, **kwargs):
    #     pk = kwargs.pop('kpj', None)

    #     super(DataTKForm, self).__init__(*args, **kwargs)
    #     if pk:
    #         kpj_pk = NoKPJ.objects.get(pk=pk)
    #         self.fields['kpj'].queryset = kpj_pk

    class Meta:
        model = DataTK
        # fields = '__all__'
        exclude = ('kpj',)
        widgets = {
            'alamat': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Alamat'
            }),
            'nama_ibu': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nama Ibu Kandung'
            }),
            'nama_pasangan': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nama Suami/Istri'
            }),
            'tgl_lahir_pasangan': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
            'nama_anak_s': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nama Anak Pertama'
            }),
            'tgl_lahir_s': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
            'nama_anak_d': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nama Anak Kedua'
            }),
            'tgl_lahir_d': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            # 'no_kpj': forms.TextInput(attrs={
            #     'class': 'form-control', 'placeholder': 'Input No KPJ'
            # }),
        }


class KPJForm(forms.ModelForm):
    nama = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Nama Lengkap',
    }))

    class Meta:
        model = NoKPJ
        exclude = ('user_kpj',)
        # fields = '__all__'

        widgets = {
            'no_kpj': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Input No KPJ'
            }),
            'is_aktif': forms.Select(attrs={
                'class': 'form-control',
            }),
            'blth_keps': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
            'blth_na': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            })
        }
