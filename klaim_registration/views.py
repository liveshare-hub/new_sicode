from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.db.models import Subquery, OuterRef, IntegerField
from django.http import JsonResponse
# from dal import autocomplete
import random
import string

from django.core import serializers
from django.forms import inlineformset_factory, modelformset_factory

from .form import DataKlaimForm, DataTKForm, KPJForm
from .models import DataKlaim, ApprovalHRD, toQRCode, DataTK, NoKPJ
from authentication.models import Perusahaan, Profile
from .decorators import admin_only

from django.core.mail import EmailMessage, EmailMultiAlternatives

from django.conf import settings

from django.template.loader import render_to_string
from email.mime.image import MIMEImage
from django.utils.html import strip_tags
from email.mime.base import MIMEBase
from email import encoders


@login_required(login_url='/accounts/login/')
def index(request):
    user = request.user
    # is_admin = User.objects.filter(username=user, is_superuser=True).exists()

    # is_hrd = Profile.objects.select_related(
    #     'user').filter(user__username=user, is_hrd=True)
    if user.is_superuser:
        datas = DataKlaim.objects.select_related('data_tk').all()
        size = datas.count()
    elif user.profile.is_hrd:
        qs = Profile.objects.select_related('npp').get(
            user__username=user, is_hrd=True)
        datas = DataKlaim.objects.select_related(
            'data_tk').filter(data_tk__kpj__user_kpj__npp_id=qs.npp_id)
        size = datas.count()

    else:
        datas = DataKlaim.objects.select_related('data_tk').filter(user=user).annotate(status_approve=Subquery(
            ApprovalHRD.objects.filter(klaim_id=OuterRef('pk')).values('status')[:1]))
        # datas = DataKlaim.objects.
        size = datas.count()
    context = {
        'datas': datas,
        'size': size,
    }

    return render(request, 'klaim_registration/index.html', context)


@login_required(login_url='/accounts/login/')
@admin_only
def listKPJ(request):
    if request.user.profile.is_hrd:
        datas_aktif = NoKPJ.objects.select_related(
            'user_kpj').filter(user_kpj__npp_id=request.user.profile.npp_id)
        datas_na = NoKPJ.objects.select_related('user_kpj').filter(
            user_kpj__npp_id=request.user.profile.npp_id, is_aktif=False)
        datas_tk = DataTK.objects.select_related('kpj').filter(
            kpj__user_kpj__npp_id=request.user.profile.npp_id)
    context = {
        'datas': datas_aktif,
        'datas_na': datas_na,
        'datatk': datas_tk
    }
    return render(request, 'klaim_registration/list_kpj.html', context)


@login_required(login_url='/accounts/login/')
@admin_only
def ListDataTerkini(request):
    user = request.user
    # print(user.profile.npp_id)
    datas = DataTK.objects.select_related('kpj').filter(
        kpj__user_kpj__npp_id=user.profile.npp_id)
    context = {
        'datas': datas
    }
    return render(request, 'klaim_registration/pengkinian_tk.html', context)


def formDaftarKPJ(request):
    npp_id = request.user.profile.npp_id

    return render(request, 'klaim_registration/daftar_kpj.html', {'npp_id': npp_id})


@login_required(login_url='/accounts/login/')
@admin_only
def daftarKPJ(request):
    msg = None
    # npp_id = request.user.profile.npp
    # print(npp_id)
    if request.method == 'POST':
        no_kpj = request.POST['no_kpj']
        nama = request.POST['nama']
        nik = request.POST['nik']
        npp = request.POST['npp']
        blth_keps = request.POST['blth_keps']
        blth_na = request.POST['blth_na']
        is_aktif = request.POST['is_aktif']
        if is_aktif == 1:
            is_aktif = True
        else:
            is_aktif = False
        cek = NoKPJ.objects.filter(no_kpj=no_kpj)
        if cek.exists():
            msg = 'No KPJ Sudah terdaftar'
        else:
            x = list(nama)
            m = (x[0]+x[1]).upper()
            str_digits = string.digits
            username = m+(''.join(random.choice(str_digits)for i in range(6)))
            # password = ''.join(random.choice(str_digits)for i in range(6))
            password = "WELCOME1"
            password_hash = make_password(password, salt=[username])
            buat_user = User.objects.create(
                username=username, password=password_hash)
            Profile.objects.update_or_create(user__username=username, defaults={
                'npp_id': npp, 'nik': nik, 'nama': nama, 'is_hrd': False})
            try:
                profile = Profile.objects.select_related(
                    'user').filter(user__username=username).first()
                print(profile)
                kpj = NoKPJ.objects.create(
                    user_kpj_id=profile.id, no_kpj=no_kpj, blth_keps=blth_keps, blth_na=blth_na, is_aktif=is_aktif)
                print(kpj)
            except:
                pass
            msg = 'KPJ berhasil di input'
            response = {
                'msg': msg
            }
            return JsonResponse(response)

    #     form = KPJForm(request.POST)
    #     if form.is_valid():
    #         post = form.save(commit=False)
    #         nama = request.POST.get('nama')
    #         nik = request.POST.get('nik')
            # x = list(nama)
            # m = (x[0]+x[1]).upper()
            # str_digits = string.digits
            # username = m+(''.join(random.choice(str_digits)for i in range(6)))
            # password = make_password('WELCOME1', salt=[username])
            # buat_user = User.objects.create(
            #     username=username, password=password)
    #         print(buat_user.id)
    #         cek = Profile.objects.filter(user_id=buat_user.id)
    #         if cek.exists():
    #             post.user_kpj_id = cek[0].id
    #         else:

    # post.user_kpj.user_id = buat_user.id
    # post.user_kpj.npp__id = request.user.profile.npp_id
    # print(post.user_kpj.npp_id)
    # post.user_kpj.nama = nama
    # post.user_kpj.is_hrd = False
    # post.user_kpj.save()
    # post.save()

    #         return redirect(reverse('list-kpj'))
    # else:
    #     form = KPJForm()
    # return render(request, 'klaim_registration/daftar_kpj.html')


@login_required(login_url='/accounts/login/')
@admin_only
def tambahKPJ(request, pk):
    user = Profile.objects.get(pk=pk)
    # npp = user.npp
    # print(user)
    KpjInlineFormset = inlineformset_factory(
        Profile, NoKPJ, fields=('no_kpj', 'blth_keps', 'blth_na', 'is_aktif',), extra=1)

    # formset = KpjInlineFormset(
    # queryset=Profile.objects.none(), instance=user)
    if request.method == 'POST':
        formset = KpjInlineFormset(
            request.POST or None, instance=user)
        if formset.is_valid():

            formset.save()
            return redirect(reverse('list-kpj'))
    else:
        formset = KpjInlineFormset(queryset=Profile.objects.none())
    return render(request, 'klaim_registration/input_kpj.html', {'forms': formset})


@login_required(login_url='/accounts/login/')
@admin_only
def tambahKlaim(request):
    user = request.user
    # cekKlaim = ApprovalHRD.objects.select_related('klaim__user').filter(
    #     klaim__user__username=user, status='DISETUJUI')
    # if cekKlaim.exists():
    #     messages.warning(request, "Akun anda sudah pernah mengajukan KLAIM")
    #     return redirect(reverse('home-klaim'))
    # print(user.is_authenticated)
    if request.method == 'POST':
        forms = DataKlaimForm(request.POST, request.FILES)
        if forms.is_valid():
            post = forms.save(commit=False)
            # post.user = user
            post.user = user

            # post.npp = request.POST['npp']
            post.save()
            # hrd = DaftarHRD.objects.get(npp_id=post.npp_id)
            ApprovalHRD.objects.create(klaim_id=post.id, hrd_id=post.npp_id)
            toQRCode.objects.create(tk_klaim_id=post.id)

            return redirect('home')

    else:
        forms = DataKlaimForm()
    return render(request, 'klaim_registration/daftar.html', {'forms': forms})


@login_required(login_url='/accounts/login/')
@admin_only
def TambahTK(request):
    user = Profile.objects.get(user=request.user)
    npp = user.npp_id
    # data = NoKPJ.objects.all()
    # data_kpj = NoKPJ.objects.get(pk=pk)
    if request.method == 'POST':
        form = DataTKForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.kpj_id = form.cleaned_data['kpj'].id
            post.nik = form.cleaned_data['nik']
            post.alamat = form.cleaned_data['alamat']
            post.nama_ibu = form.cleaned_data['nama_ibu']
            post.status = form.cleaned_data['status']
            post.npp_id = npp
            post.nama_pasangan = form.cleaned_data['nama_pasangan']
            post.tgl_lahir_pasangan = form.cleaned_data['tgl_lahir_pasangan']
            post.nama_anak_s = form.cleaned_data['nama_anak_s']
            post.tgl_lahir_s = form.cleaned_data['tgl_lahir_s']
            post.nama_anak_d = form.cleaned_data['nama_anak_d']
            post.tgl_lahir_d = form.cleaned_data['tgl_lahir_d']
            post.save()
            return redirect(reverse(('home')))
    else:
        form = DataTKForm()
    return render(request, 'klaim_registration/daftar_tk.html', {'form': form})


def PengkinianTK(request, pk):
    # qs = get_object_or_404(DataTK, kpj__user_kpj_id=pk)
    qs = NoKPJ.objects.select_related(
        'user_kpj').filter(user_kpj_id=pk).first()
    if qs.user_kpj.tempat_lahir == '':
        messages.WARNING(request, "Update Profile terlebih dahulu!")
        return redirect(reverse('list-kpj'))
    elif request.method == 'POST':
        form = DataTKForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.kpj_id = qs.id
            post.alamat = form.cleaned_data['alamat']
            post.nama_ibu = form.cleaned_data['nama_ibu']
            post.status = form.cleaned_data['status']
            post.nama_pasangan = form.cleaned_data['nama_pasangan']
            post.tgl_lahir_pasangan = form.cleaned_data['tgl_lahir_pasangan']
            post.nama_anak_s = form.cleaned_data['nama_anak_s']
            post.tgl_lahir_s = form.cleaned_data['tgl_lahir_s']
            post.nama_anak_d = form.cleaned_data['nama_anak_d']
            post.tgl_lahir_d = form.cleaned_data['tgl_lahir_d']
            post.save()
            return redirect(reverse(('list-pengkinian')))
    else:
        form = DataTKForm(instance=qs)
    return render(request, 'klaim_registration/daftar_tk.html', {'form': form, 'qs': qs})


@ login_required(login_url='/accounts/login/')
@ admin_only
def DaftarTk(request):
    datas = DataTK.objects.all()
    context = {
        'datas': datas
    }
    return render(request, 'klaim_registration/list_tk.html', context)


@ login_required(login_url='/accounts/login/')
@ admin_only
def tambahKlaim1(request):
    if request.method == 'POST':
        forms = DataKlaimForm(request.POST, request.FILES)
        if forms.is_valid():
            post = forms.save(commit=False)
            random_str = string.digits
            username = 'user_'+(''.join(random.choice(random_str)
                                        for i in range(4)))
            password = make_password('WELCOME1', salt=[username])
            cekUser = User.objects.all().filter(username=username)
            if cekUser.exists():
                messages.WARNING(request, "USER SUDAH DIPAKAI")
            else:
                buat_user = User.objects.create(
                    username=username, password=password
                )
                # post.user_id = buat_user.id
                post.profile.user_id = buat_user.id
                # print(post.user_id)
                group = Group.objects.get(name='TK')
                buat_user.groups.add(group)

                post.save()
                ApprovalHRD.objects.create(
                    klaim_id=post.id, hrd_id=post.npp_id)
                toQRCode.objects.create(tk_klaim_id=post.id)
                # data = toQRCode.objects.select_related('tk_klaim').get(
                #     tk_klaim__klaim__user__id=post.user_id)
                # print(data)
                # send_mail(data)
            return redirect('get-detail')
    else:
        forms = DataKlaimForm()
    return render(request, 'klaim_registration/daftar.html', {'forms': forms})


@ login_required(login_url='/accounts/login/')
def daftarKlaimHRD(request):
    # print(request.user)
    datas = ApprovalHRD.objects.select_related('hrd').filter(
        hrd__user__username=request.user, status='DALAM PEMERIKSAAN')
    if not datas.exists():
        datas = ApprovalHRD.objects.select_related(
            'hrd__user').filter(hrd__user__username=request.user)
        # detail = datas.select_related('klaim')
        # print(detail)
    if request.is_ajax:
        # print(request.POST.get('status'))
        ApprovalHRD.objects.filter(id=request.POST.get('id')).update(
            status=request.POST.get('status'), keterangan=request.POST.get('keterangan'))
        # return JsonResponse({'data': 'sucess'})
    context = {
        'datas': datas,
        # 'detail':detail,
    }

    return render(request, 'klaim_registration/hrd.html', context)


@ login_required(login_url='/accounts/login/')
def daftarKlaimHRD1(request):
    # print(request.user)
    datas = ApprovalHRD.objects.all().filter(
        hrd__user__username=request.user, status='DALAM PEMERIKSAAN')
    if not datas.exists():
        datas = ApprovalHRD.objects.all().filter(hrd__user__username=request.user)
        detail = datas.select_related('klaim')
        # print(detail)
    if request.is_ajax:
        # print(request.POST.get('status'))
        ApprovalHRD.objects.filter(id=request.POST.get('id')).update(
            status=request.POST.get('status'), keterangan=request.POST.get('keterangan'))
        # return JsonResponse({'data': 'sucess'})
    context = {
        'datas': datas,
        'detail': detail,
    }

    return render(request, 'klaim_registration/hrd1.html', context)


# @ login_required(login_url='/accounts/login/')
# def get_detail_tk(request, id=None):
#     instance = get_object_or_404(DataKlaim, id=id)
#     context = {
#         'instance': instance
#     }
#     return render(request, 'klaim_registration/modal.html', context)

@ login_required(login_url='/accounts/login/')
@ admin_only
def get_klaimhrd_json(request, klaim_id):
    hrd_qs = list(toQRCode.objects.select_related('tk_klaim').filter(tk_klaim__hrd__user__username=request.user, tk_klaim__klaim_id=klaim_id).values(
        'tk_klaim_id', 'tk_klaim__klaim__nama', 'tk_klaim__klaim__nik', 'tk_klaim__klaim__kpj', 'tk_klaim__klaim__npp', 'tk_klaim__klaim__tempat_lahir', 'tk_klaim__klaim__tgl_lahir',
        'tk_klaim__klaim__nama_ibu', 'tk_klaim__klaim__status', 'tk_klaim__klaim__nama_rekening', 'tk_klaim__klaim__no_rekening', 'tk_klaim__klaim__no_hp'
    ))

    return JsonResponse({'data': hrd_qs})


@ login_required(login_url='/accounts/login/')
@ admin_only
def DataTKJson(request):
    npp = request.user.profile.npp
    tk_json = list(NoKPJ.objects.select_related('npp').filter(
        npp=npp).values('npp__nama', 'no_kpj', 'is_aktif'))

    return JsonResponse({'data': tk_json})


def PengkinianJson(request):
    user = request.user
    pengkinian_json = list(DataTK.objects.select_related('kpj').filter(
        kpj__user_kpj__npp_id=user.profile.npp_id).values('kpj__id', 'kpj__no_kpj', 'kpj__user_kpj__nama', 'kpj__user_kpj__nik', 'alamat', 'nama_ibu', 'status',
                                                          'nama_pasangan', 'tgl_lahir_pasangan', 'nama_anak_s', 'tgl_lahir_s', 'nama_anak_d', 'tgl_lahir_d'))
    for data in pengkinian_json:
        if data['status'] == '1':
            data['status'] = 'BELUM MENIKAH'
        else:
            data['status'] = 'MENIKAH'
    return JsonResponse({'data': pengkinian_json})


def PengajuanKlaim(request, pk):
    qs = DataTK.objects.select_related(
        'kpj').filter(kpj__id=pk).first()
    # print(qs.id)
    if request.method == 'POST':
        form = DataKlaimForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.data_tk_id = qs.id
            post.tipe_klaim = form.cleaned_data['tipe_klaim']
            post.sebab_klaim = form.cleaned_data['sebab_klaim']
            post.email = form.cleaned_data['email']
            post.nama_rekening = form.cleaned_data['nama_rekening']
            post.no_rekening = form.cleaned_data['no_rekening']
            post.file_kk = form.cleaned_data['file_kk']
            post.file_ktp = form.cleaned_data['file_ktp']
            post.file_paklaring = form.cleaned_data['file_paklaring']
            post.file_lain = form.cleaned_data['file_lain']
            post.save()

            return redirect(reverse('home'))
    else:
        form = DataKlaimForm(instance=qs)
        return render(request, 'klaim_registration/daftar.html', {'form': form, 'qs': qs})


@ login_required(login_url='/accounts/login/')
@ admin_only
def get_detail_tk(request):
    datas = toQRCode.objects.select_related('tk_klaim').filter(
        tk_klaim__hrd__user__username=request.user, tk_klaim__status='DALAM PEMERIKSAAN')
    if datas.exists():
        datas = toQRCode.objects.select_related('tk_klaim').filter(
            tk_klaim__hrd__user__username=request.user)
    else:
        datas = toQRCode.objects.none()

    if request.is_ajax:

        ApprovalHRD.objects.filter(id=request.POST.get('id')).update(
            status=request.POST.get('status'), keterangan=request.POST.get('keterangan'))

    context = {
        'datas': datas
    }
    return render(request, 'klaim_registration/hrd.html', context)


@ login_required(login_url='/accounts/login/')
def daftarSeluruhKlaim(request):
    is_hrd = ApprovalHRD.objects.all().filter(
        hrd__user__username=request.user)[0]
    # print(is_hrd)
    if is_hrd:
        datas = is_hrd.all()
        return render(request, 'klaim_registration/hrd.html', {'datas': datas})
    else:
        return redirect('home')


def qrcode_display(request, id):

    qr_qs = list(toQRCode.objects.select_related('tk_klaim__klaim').filter(
        tk_klaim__hrd__user__username=request.user, id=id).values('tk_klaim_id', 'tk_klaim', 'url_uuid', 'img_svg'))

    return JsonResponse({'data': qr_qs})


@ login_required(login_url='/accounts/login/')
def detail_tk(request, uid):
    datas = toQRCode.objects.select_related('tk_klaim').filter(
        url_uuid=uid)

    context = {
        'datas': datas
    }
    return render(request, 'klaim_registration/detail_tk.html', context)


def sent_mail(request, id):
    data = toQRCode.objects.select_related('tk_klaim').get(
        tk_klaim__klaim__user__id=id)
    # qrcode = '/home/sicm6455/python/' + data.img_svg.url
    qrcode = data.img_svg.url
    to = data.tk_klaim.klaim.email
    context = {
        'nama': data.tk_klaim.klaim.nama,
        'username': data.tk_klaim.klaim.user.username,
        'qrcode': qrcode
    }
    html_content = render_to_string('klaim_registration/email.html', context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        # subject
        "AKUN ANDA SUDAH TERDAFTAR",
        # content,
        text_content,
        # from email,
        settings.EMAIL_HOST_USER,
        # rec lists
        [to]
    )
    email.attach_alternative(html_content, "text/html")
    filename = '/home/sicm6455/python/' + data.img_svg.url
    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= "+filename)

    email.attach(part)
    # msg_img = MIMEImage(qrcode.file)
    # msg_img.add_header('Content-ID', '<{}>'.format(qrcode.name))
    # email.attach(msg_img)
    # email.attach_file(data.img_svg.url)
    email.send()
    # messages.SUCCESS(request, "Email berhasil dikirim !")

    return redirect('/')
