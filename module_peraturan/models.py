from django.db import models
from ckeditor.fields import RichTextField
from datetime import datetime
from jdih_libs.utils import list_tahun
from django.core.validators import FileExtensionValidator
from django.conf import settings
from module_admin_list.models import UserJDIHCostum
from django.utils.html import format_html

# Create your models here.
class KategoriPeraturan(models.Model):
	parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Kelompok Menu', null=True, blank=True, )
	category_name = models.CharField(verbose_name='Kategori Menu', max_length=255)
	urutan = models.IntegerField()

	def __str__(self):
		return self.category_name

	class Meta:
		db_table = 'jdih_kategori_peraturan'
		verbose_name_plural = 'Kategori Peraturan'


	def kelompok_menu(self):
		if not self.parent is None:
			return self.parent.category_name+"/"+self.category_name
		else:
			return self.category_name

	def kategori_menu(self):
		if not self.parent is None:
			return "Sub Kategori: "+self.category_name
		else:
			return "-"


class DataListPeraturan(models.Model):
	subject = models.CharField(max_length=255, help_text='Isikan judul/subject tentang peraturan yang diupload')
	kategori = models.ForeignKey(KategoriPeraturan, on_delete=models.CASCADE, help_text='kategori/jenis peraturan yang diupload')
	tahun_peraturan = models.IntegerField(help_text='tahun peraturan dikeluarkan', choices=list_tahun(), default=(datetime.now().year))
	nomor_peraturan = models.CharField(max_length=255, help_text='nomor peraturan dikeluarkan')
	dokument = models.FileField(help_text='upload full dokument peraturan yang akan diunduh client',\
				validators=[FileExtensionValidator(['pdf','docs','docx'])], upload_to=settings.FILE_DOKUMEN)	
	list_status_peraturan = (
		('-', ('')),
		('dicabut', ('Dicabut')),
		('mencabut', ('Mencabut')),
		('diubah', ('Diubah')),
		('mengubah', ('Mengubah')),
		('batal', ('Batal')),
	)
	status = models.CharField(max_length=50, choices=list_status_peraturan, default='-')

	catalog_tajuk_entri = models.CharField(max_length=255, null=True, blank=True,verbose_name="Tajuk Entri Utama")
	catalog_judul_seragam = models.CharField(max_length=255, null=True, blank=True,verbose_name="Judul Seragam")
	catalog_bentuk_nomor_tahun = models.CharField(max_length=255, null=True, blank=True,verbose_name="Bentuk, Nomor, Tahun Peraturan")
	catalog_tanggal_bulan_tahun = models.CharField(max_length=255, null=True, blank=True,verbose_name="Tanggal, Bulan, dan Tahun Peraturan")
	catalog_perihal = models.CharField(max_length=255, null=True, blank=True,verbose_name="Perihal / Tentang")
	catalog_pengesahan = models.CharField(max_length=255, null=True, blank=True,verbose_name="Tempat Pengesahan")
	catalog_tahun_pengesahan = models.CharField(max_length=255, null=True, blank=True,verbose_name="Tahun Peraturan")
	catalog_sumber_teks = RichTextField(null=True, blank=True,verbose_name="Sumber Teks Peraturan")
	catalog_subject = models.CharField(max_length=255, null=True, blank=True,verbose_name="Subjek Peraturan")
	catalog_singkatan_peraturan = models.CharField(max_length=255, null=True, blank=True,verbose_name="Singkatan Bentuk Peraturan")
	catalog_lokasi_penyimpanan = models.CharField(max_length=255, null=True, blank=True,verbose_name="Lokasi Penyimpanan")
	abstract_subject = models.CharField(max_length=255, null=True, blank=True,verbose_name="Subjek Abstrak Peraturan")
	abstract_tahun = models.CharField(max_length=255, null=True, blank=True,verbose_name="Tahun Abstrak Peraturan")
	abstract_singkatan_peraturan = models.CharField(max_length=255, null=True, blank=True,verbose_name="Singkatan Bentuk Peraturan")
	abstract_nomor = models.CharField(max_length=255, null=True, blank=True,verbose_name="Nomor Peraturan")
	abstract_sumber = models.CharField(max_length=255, null=True, blank=True,verbose_name="Sumber Peraturan")
	abstract_jumlah_halaman = models.CharField(max_length=255, null=True, blank=True,verbose_name="Jumlah Halaman Peraturan")
	abstract_jenis = models.CharField(max_length=255, null=True, blank=True,verbose_name="Jenis/Bentuk Peraturan")
	abstract_tentang = RichTextField(null=True, blank=True,verbose_name="Tentang Peraturan")
	abstract_deskripsi = RichTextField(null=True, blank=True,verbose_name="Abstrak Peraturan ini Adalah")
	abstract_dasar_hukum =RichTextField(null=True, blank=True,verbose_name="Dasar Hukum Undang-Undang ini adalah")
	abstract_diatur = RichTextField(null=True, blank=True,verbose_name="Dalam Undang-Undang ini diatur tentang")
	abstract_catatan = RichTextField(null=True, blank=True,verbose_name="CATATAN")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	created_by = models.ForeignKey(UserJDIHCostum, on_delete=models.CASCADE, editable=False)
	updated_by = models.ForeignKey(UserJDIHCostum, related_name='admin_peraturan_updated', on_delete=models.CASCADE, editable=False, null=True)




	def __str__(self):
		return self.subject

	class Meta:
		db_table = 'jdih_data_peraturan'
		verbose_name_plural = 'Data Peraturan'


	def riwayat_data_peraturan(self):
		created = (self.created_at).strftime("%d %B %Y jam %H:%M")
		if self.updated_by is None:
			update_on = '-'
		else:
			update_on = (self.updated_at).strftime("%d %B %Y jam %H:%M")
			update_on = f"<b>{self.updated_by}</b> pada {update_on}"

		return format_html(f"dibuat : <b>{self.created_by}</b> pada {created}</br>\
							diedit : {update_on}") 

	def tanggal_posting(self):
		return (self.created_at).strftime("%d %B %Y jam %H:%M")