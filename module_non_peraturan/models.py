from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class NonPeraturan(models.Model):
	subject = models.CharField(max_length=255, help_text='Isikan judul/subject tentang peraturan yang diupload',verbose_name='*Judul/Subjek')
	dokument = models.FileField(help_text='upload full dokument peraturan yang akan diunduh client',verbose_name='*Full Document Non-Peraturan')
	thumbnail = models.ImageField(help_text='upload gambar tampilan dari buku/produk hukum non-peraturan',verbose_name='*Input Thumbnail Non-Peraturan')


	col_number = models.CharField(max_length=255, null=True, blank=True,verbose_name='Col. Number')
	authors = models.CharField(max_length=255,verbose_name='* Pengarang Buku')
	judul_buku = models.CharField(max_length=255, null=True, blank=True,verbose_name='Judul Buku')
	kota_terbit = models.CharField(max_length=255, null=True, blank=True,verbose_name='Kota Terbit')
	penerbit_buku = models.CharField(max_length=255, null=True, blank=True,verbose_name='Penerbit Buku')
	tahun_terbit = models.CharField(max_length=255, null=True, blank=True,verbose_name='Tahun Terbit Buku')
	jilid = models.CharField(max_length=255, null=True, blank=True,verbose_name='Jilid')
	jumlah_halaman = models.IntegerField(null=True, blank=True,verbose_name='Jumlah Halaman Buku')
	tebal_buku = models.CharField(max_length=255, null=True, blank=True,verbose_name='Tebal Buku')
	subject_pengarang_buku = RichTextField(null=True, blank=True,verbose_name='Subjek & Pengarang Buku')
	nomor_induk = models.CharField(max_length=255, null=True, blank=True,verbose_name='Nomor Induk')
	status = models.CharField(max_length=255, null=True, blank=True,verbose_name='Status Buku')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	def __str__(self):
		return self.subject

	class Meta:
		db_table = 'jdih_data_non_peraturan'
		verbose_name_plural = 'Data Non Peraturan'
		verbose_name = 'Data Non Peraturan'


	def riwayat_data_peraturan(self):
		return "data belum tersedia saat ini"

	def tanggal_posting(self):
		return (self.created_at).strftime("%d %B %Y jam %H:%M")