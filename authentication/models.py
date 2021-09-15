# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.models import AbstractUser
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image as Img
from io import BytesIO
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
import datetime


NIK_VALIDATOR = RegexValidator("^\d{16}$",
                               "Format NIK Tidak Sesuai")

HP_VALIDATOR = RegexValidator(
    "^(08+[1-9])([0-9]{7,10})$", "Format NO HP TIDAK SESUA!!!")

YA_TIDAK = (
    (True, 'Y'),
    (False, 'T')
)


class Perusahaan(models.Model):
    nama = models.CharField(max_length=200)
    npp = models.CharField(max_length=8)

    class Meta:
        ordering = ['-npp']
        verbose_name = "NPP"
        verbose_name_plural = "LIST NPP"

    def __str__(self):
        return self.nama


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    npp = models.ForeignKey(
        Perusahaan, on_delete=models.CASCADE, blank=True, null=True)
    propic = models.ImageField(
        upload_to='profile/hrd/', blank=True, null=True)
    nama = models.CharField(max_length=100)
    tgl_lahir = models.DateField(null=True, blank=True,
                                 default=datetime.datetime.strptime('01-01-1900', '%d-%m-%Y'))
    tempat_lahir = models.CharField(max_length=100, blank=True, null=True)
    nik = models.CharField(max_length=16, validators=[
                           NIK_VALIDATOR], blank=True, null=True)
    no_hp = models.CharField(max_length=15, validators=[
                             HP_VALIDATOR], blank=True, null=True)
    is_hrd = models.BooleanField(default=True, choices=YA_TIDAK)

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.npp)

    def save(self, *args, **kwargs):
        width = 250
        height = 250
        size = (width, height)
        isSame = False
        if self.propic:
            try:
                this = Profile.objects.get(id=self.id)
                if this.propic == self.propic:
                    isSame = True
            except:
                pass

            image = Img.open(
                BytesIO(self.propic.read()))
            (imw, imh) = image.size
            if (imw > width) or (imh > height):
                image.thumbnail(size, Img.ANTIALIAS)

            # If RGB, convert transparancy
            if image.mode == 'RGBA':
                image.load()
                background = Img.new("RGB", image.size, (255, 255, 255))
                # 3 is the alpha channel
                background.paste(image, mask=image.split()[3])
                image = background

            output = BytesIO()
            image.save(output, format='JPEG', quality=80)
            output.seek(0)
            self.propic = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.propic.name.split('.')[
                                               0], 'image/jpeg', output.getvalue, None)
        try:
            this = Profile.objects.get(id=self.id)
            if this.propic == self.propic or isSame:
                self.propic = this.propic
            else:
                this.propic.delete(save=False)
        except:
            pass

        super().save(*args, **kwargs)

        @receiver(post_delete, sender=Profile)
        def propic_post_delete_handler(sender, **kwargs):
            instance = kwargs['instance']
            try:
                storage, path = instance.propic.storage, instance.propic.path
                if (path != '.') and (path != '/') and (path != 'profile/') and (path != 'profile/.'):
                    storage.delete(path)
            except:
                pass


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# post_save.connect(create_profile, sender=User)

@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    if created == False:
        instance.profile.save()


class ProfileTK(models.Model):
    user_tk = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    tgl_lahir = models.DateField()
    tempat_lahir = models.CharField(max_length=100)
    propic = models.ImageField(
        upload_to='profile/tk/', blank=True, null=True)

    def __str__(self):
        return self.nama

    def save(self, *args, **kwargs):
        width = 250
        height = 250
        size = (width, height)
        isSame = False
        if self.propic:
            try:
                this = ProfileTK.objects.get(id=self.id)
                if this.propic == self.propic:
                    isSame = True
            except:
                pass

            image = Img.open(
                BytesIO(self.propic.read()))
            (imw, imh) = image.size
            if (imw > width) or (imh > height):
                image.thumbnail(size, Img.ANTIALIAS)

            # If RGB, convert transparancy
            if image.mode == 'RGBA':
                image.load()
                background = Img.new("RGB", image.size, (255, 255, 255))
                # 3 is the alpha channel
                background.paste(image, mask=image.split()[3])
                image = background

            output = BytesIO()
            image.save(output, format='JPEG', quality=80)
            output.seek(0)
            self.propic = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.propic.name.split('.')[
                                               0], 'image/jpeg', output.getvalue, None)
        try:
            this = ProfileTK.objects.get(id=self.id)
            if this.propic == self.propic or isSame:
                self.propic = this.propic
            else:
                this.propic.delete(save=False)
        except:
            pass
        super().save(*args, **kwargs)
