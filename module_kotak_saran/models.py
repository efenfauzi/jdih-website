from django.db import models

# Create your models here.
class KotakSaran(models.Model):
	judul = models.CharField(max_length=100)
	nama_pengirim = models.CharField(max_length=100)
	email_pengirim = models.CharField(max_length=100)
	subyek = models.CharField(max_length=100)
	content = models.TextField()
	post_date = models.DateTimeField(auto_now_add=True)
	status_terbaca = models.IntegerField()


	def __str__(self):
		return self.judul

	class Meta:
		db_table = 'jdih_kotak_saran'
		verbose_name_plural = 'Inbox Kotak Saran'
		verbose_name = 'Inbox Kotak Saran'