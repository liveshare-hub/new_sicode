# Generated by Django 3.2.3 on 2021-09-14 07:09

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perusahaan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=200)),
                ('npp', models.CharField(max_length=8)),
            ],
            options={
                'verbose_name': 'NPP',
                'verbose_name_plural': 'LIST NPP',
                'ordering': ['-npp'],
            },
        ),
        migrations.CreateModel(
            name='ProfileTK',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('tgl_lahir', models.DateField()),
                ('tempat_lahir', models.CharField(max_length=100)),
                ('propic', models.ImageField(blank=True, null=True, upload_to='profile/tk/')),
                ('user_tk', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('propic', models.ImageField(blank=True, null=True, upload_to='profile/hrd/')),
                ('nama', models.CharField(max_length=100)),
                ('tgl_lahir', models.DateField(blank=True, default=datetime.datetime(1900, 1, 1, 0, 0), null=True)),
                ('tempat_lahir', models.CharField(blank=True, max_length=100, null=True)),
                ('nik', models.CharField(blank=True, max_length=16, null=True, validators=[django.core.validators.RegexValidator('^\\d{16}$', 'Format NIK Tidak Sesuai')])),
                ('no_hp', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator('^(08+[1-9])([0-9]{7,10})$', 'Format NO HP TIDAK SESUA!!!')])),
                ('is_hrd', models.BooleanField(choices=[(True, 'Y'), (False, 'T')], default=True)),
                ('npp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.perusahaan')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
