from django.db import models
from ckeditor.fields import RichTextField
from jdih_libs.models_helpers import url_handler_template


# Create your models here.
class KontenDinamis(models.Model):
	menu = models.CharField(max_length=30, help_text="Menu akan muncul sebagai halaman", 
							verbose_name="nama menu")
	konten = RichTextField(null=True)
	urutan_menu = models.IntegerField()

	def __str__(self):
		return self.menu

	class Meta:
		db_table = 'jdih_konten_dinamis'
		verbose_name_plural = 'Konten Dinamis'

	def save(self, *args, **kw):
		super(KontenDinamis, self).save(*args, **kw)
		url_handler_template(self.__class__.__name__, self.menu, self.pk)
