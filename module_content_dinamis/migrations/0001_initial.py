# Generated by Django 3.1.2 on 2020-10-12 19:15

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KontenDinamis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu', models.CharField(help_text='Menu akan muncul sebagai halaman', max_length=30, verbose_name='nama menu')),
                ('konten', ckeditor.fields.RichTextField(null=True)),
                ('urutan_menu', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Konten Dinamis',
                'db_table': 'jdih_konten_dinamis',
            },
        ),
    ]
