from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from PIL import Image, ImageDraw
import uuid
import qrcode
from io import BytesIO
from django.core.files import File

from authentication.models import Profile, Perusahaan, ProfileTK
# from .uuid_gen import autoGen

NIK_VALIDATOR = RegexValidator("^\d{16}$",
                               "Format NIK Tidak Sesuai")

HP_VALIDATOR = RegexValidator(
    "^(08+[1-9])([0-9]{7,9})$", "Format NO HP TIDAK SESUA!!!")

NO_REK_VALIDATOR = RegexValidator("^\d{6,}$", "No Rekening Harus Berupa Angka")

EKSTENSI_VALIDATOR = RegexValidator(
    ".*\.(jpg|JPG|JPEG|pdf|PDF)", "Only Support PDF dan JPG")

SEGMEN = (
    ('PU', 'PENERIMA UPAH'),
    ('BPU', 'BUKAN PENERIMA UPAH'),
    ('JAKON', 'JASA KONSTRUKSI'),
)

TIPE_KLAIM = (
    ('JHT01', 'JHT'),
    ('JKK01', 'JKK'),
    ('JKM01', 'JKM'),
    ('JPN01', 'JPN'),
)


STATUS = (
    ('1', 'BELUM MENIKAH'),
    ('2', 'MENIKAH')
)

STATUS_APPROVAL = (
    ('DALAM PEMERIKSAAN', 'DALAM PEMERIKSAAN'),
    ('DISETUJUI', 'DISETUJUI'),
    ('DITOLAK', 'DITOLAK')
)

AKTIF_NA = (
    (False, 'Tidak Aktif'),
    (True, 'Aktif')
)


class SebabKlaim(models.Model):
    kode = models.CharField(max_length=5)
    keterangan = models.CharField(max_length=200)
    keyword = models.CharField(max_length=3)

    def __str__(self):
        return '{} - {}'.format(self.kode, self.keterangan)


class NoKPJ(models.Model):
    user_kpj = models.ForeignKey(Profile, on_delete=models.CASCADE)
    no_kpj = models.CharField(max_length=15)
    blth_keps = models.DateField()
    blth_na = models.DateField(blank=True, null=True)
    is_aktif = models.BooleanField(choices=AKTIF_NA, default=False)

    class Meta:
        verbose_name = "KPJ"
        verbose_name_plural = "LIST KPJ"

    def __str__(self):
        return '{} - {}'.format(self.no_kpj, self.user_kpj.nama)


class DataTK(models.Model):
    kpj = models.ForeignKey(
        NoKPJ, on_delete=models.CASCADE)
    # nik = models.CharField(max_length=16, validators=[
    #                        NIK_VALIDATOR])
    # no_kpj = models.ForeignKey(NoKPJ, on_delete=models.CASCADE)
    alamat = models.CharField(max_length=250)
    nama_ibu = models.CharField(max_length=100)
    status = models.CharField(choices=STATUS, max_length=1, default='1')
    nama_pasangan = models.CharField(max_length=100, null=True, blank=True)
    tgl_lahir_pasangan = models.DateField(blank=True, null=True)
    nama_anak_s = models.CharField(max_length=100, blank=True, null=True)
    tgl_lahir_s = models.DateField(null=True, blank=True)
    nama_anak_d = models.CharField(max_length=100, blank=True, null=True)
    tgl_lahir_d = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "DATA TK"
        verbose_name_plural = "LIST DATA TK"

    def __str__(self):

        return '{} - {}'.format(self.kpj.no_kpj, self.kpj.user_kpj.nama)


# @receiver(post_save, sender=NoKPJ)
# def create_dataTk(sender, instance, created, **kwargs):
#     if created:
#         DataTK.objects.create(kpj=instance)


class DataKlaim(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_tk = models.ForeignKey(DataTK, on_delete=models.CASCADE)
    # tgl_na = models.DateField()
    email = models.EmailField(max_length=100)
    nama_rekening = models.CharField(max_length=100)
    tipe_klaim = models.CharField(max_length=5, choices=TIPE_KLAIM)
    sebab_klaim = models.ForeignKey(SebabKlaim, on_delete=models.CASCADE)
    no_rekening = models.CharField(
        max_length=16, validators=[NO_REK_VALIDATOR])
    file_kk = models.FileField(
        upload_to='kk/', validators=[EKSTENSI_VALIDATOR])
    file_ktp = models.FileField(
        upload_to='ktp/', validators=[EKSTENSI_VALIDATOR])
    file_paklaring = models.FileField(
        upload_to='vaklaring/', validators=[EKSTENSI_VALIDATOR])
    file_lain = models.FileField(
        upload_to='lain/', null=True, blank=True, validators=[EKSTENSI_VALIDATOR])
    created_on = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "DATA KLAIM"
        verbose_name_plural = "LIST DATA KLAIM"

    def __str__(self):
        return self.data_tk.kpj.user_kpj.nama


# @receiver(post_save, sender=DataTK)
# def create_dataTk(sender, instance, created, **kwargs):
#     if created:
#         DataKlaim.objects.create(data_tk=instance)
# class DaftarHRD(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     nama = models.CharField(max_length=100)
#     npp = models.ForeignKey(Perusahaan, on_delete=models.CASCADE)

#     class Meta:
#         verbose_name_plural = "LIST HRD"

#     def __str__(self):
#         return self.nama


class ApprovalHRD(models.Model):
    status = models.CharField(choices=STATUS_APPROVAL,
                              default='DALAM PEMERIKSAAN', max_length=20)
    klaim = models.ForeignKey(DataKlaim, on_delete=models.CASCADE)
    hrd = models.ForeignKey(Profile, on_delete=models.CASCADE)
    keterangan = models.TextField(null=True, blank=True)


class toQRCode(models.Model):
    tk_klaim = models.ForeignKey(ApprovalHRD, on_delete=models.CASCADE)
    url_uuid = models.UUIDField(default=uuid.uuid4(), editable=False)
    img_svg = models.ImageField(upload_to='qrcode/')

    def __str__(self):
        return self.tk_klaim.klaim.nama

    def save(self, *args, **kwargs):
        qr = qrcode.QRCode(
            version=20,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=30,
            border=4,
        )
        # qr.add_data('https://sicode.id/qr-code/{}/'.format(self.url_uuid))
        qr.add_data('http://127.0.0.1/qr-code/{}/'.format(self.url_uuid))
        qr.make(fit=False)
        # qrcode_image = qrcode.make(
        # 'http://127.0.0.1:8000/qr-code/{}/'.format(self.url_uuid))
        qrcode_image = qr.make_image(fill_color="black", back_color="white")

        canvas = Image.new('RGB', (300, 300), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_image)
        # uid = uuid.uuid4()
        fname = '{}.PNG'.format(self.tk_klaim.klaim.nama)
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        # qrcode_image.save(buffer, 'PNG')
        self.img_svg.save(fname, File(buffer), save=False)
        canvas.close()
        # qrcode_image.close()
        super().save(*args, **kwargs)


# @receiver(post_save, sender=Profile)
# def create_datatk(sender, instance, created, **kwargs):
#     if created:
        # datatk = DataTK()
        # datatk.save()
        # instance.profile = datatk
        # instance.save()
        # DataTK.objects.create(profile=instance)
