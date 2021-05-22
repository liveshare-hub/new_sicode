# Generated by Django 3.2.2 on 2021-05-13 12:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('klaim_registration', '0003_dataklaim_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataklaim',
            name='nik',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator('^\\d{16}$', 'Format NIK Tidak Sesuai')]),
        ),
        migrations.CreateModel(
            name='ApprovalHRD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('0', 'DALAM PEMERIKSAAN'), ('1', 'DISETUJUI'), ('2', 'DITOLAK')], default='0', max_length=1)),
                ('keterangan', models.TextField(blank=True, null=True)),
                ('hrd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='klaim_registration.daftarhrd')),
                ('klaim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='klaim_registration.dataklaim')),
            ],
        ),
    ]
