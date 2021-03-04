# Generated by Django 3.1.2 on 2020-10-21 13:55

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PengetahuanHukumPraktis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(help_text='Isikan judul berita hukum', max_length=255, verbose_name='Judul')),
                ('konten', ckeditor.fields.RichTextField(verbose_name='Isi')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='username_pengetahuan_hukum', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Pengetahuan Hukum Praktis',
                'verbose_name_plural': 'Pengetahuan Hukum Praktis',
                'db_table': 'jdih_pengetahuan_hukum_praktis',
            },
        ),
    ]
