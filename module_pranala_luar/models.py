from django.db import models

# Create your models here.
class PranalaLuar(models.Model):
	# FK ke Kategori/jenis peraturan
	title = models.CharField(max_length=30, verbose_name="nama url")
	url = models.URLField(max_length=150, verbose_name="alamat url/pranala luar link")
	urutan = models.IntegerField()

	def __str__(self):
		return self.title

	class Meta:
		db_table = 'jdih_pranala_luar'
		verbose_name_plural = 'Pranala Luar'
		verbose_name = 'Pranala Luar'