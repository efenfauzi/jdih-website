from django.db import models
from module_admin_list.models import UserJDIHCostum
# from django.contrib.auth.models import User as UserJDIHCostum
from ckeditor.fields import RichTextField
from django.utils.html import format_html
from django.conf import settings
from jdih_libs.utils import encode_string
from jdih_libs.models_helpers import url_handler_template


# Create your models here.

class BeritaHukum(models.Model):
	judul = models.CharField(max_length=255, help_text='Isikan judul berita hukum',verbose_name='Judul Berita')
	konten = RichTextField(verbose_name='Isi Berita')
	image = models.ImageField(null=True, blank=True, help_text="Upload gambar ukuran 480x768 atau proposionalnya sebagai header berita.", \
			verbose_name="Gambar Header Berita")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	created_by = models.ForeignKey(UserJDIHCostum, on_delete=models.CASCADE, editable=False)
	updated_by = models.ForeignKey(UserJDIHCostum, related_name='username_admin', on_delete=models.CASCADE, editable=False, null=True)


	def __str__(self):
		return self.judul

	class Meta:
		db_table = 'jdih_berita_hukum'
		verbose_name_plural = 'Berita Hukum'
		verbose_name = 'Berita Hukum'


	def riwayat_berita_hukum(self):
		created = (self.created_at).strftime("%d %B %Y jam %H:%M")
		if self.updated_by is None:
			update_on = '-'
		else:
			update_on = (self.updated_at).strftime("%d %B %Y jam %H:%M")
			update_on = f"<b>{self.updated_by}</b> pada {update_on}"

		return format_html(f"dibuat : <b>{self.created_by}</b> pada {created}</br>\
							diedit : {update_on}") 


	def preview_berita(self):
		rand_name = encode_string(self.judul) 
		if not self.image:
			img = settings.STATIC_URL+'web/img/jdhi_placeholder.png'
		else:
			img = self.image.url 
		modal_html = f"""
						<!-- Button trigger modal -->
						<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#{self.id}-{rand_name}">
						  Lihat
						</button>

						<!-- Modal -->
						<div class="modal fade" id="{self.id}-{rand_name}" tabindex="-1" role="dialog" aria-labelledby="{self.id}-{rand_name}Title" aria-hidden="true">
						  <div class="modal-dialog modal-lg" role="document">
						    <div class="modal-content">
						      <div class="modal-header">
						        <h3 class="modal-title" id="{self.id}-{rand_name}Title">{self.judul}</h3>
						        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
						          <span aria-hidden="true">&times;</span>
						        </button>
						      </div>
						      <div class="modal-body">
						      	<p><img src="{img}" class="ml-auto" style="width:100% "></p
						        <p>{self.konten}</p>
						      </div>
						      <div class="modal-footer text-center">
						        <button type="button" class="btn btn-danger" data-dismiss="modal">Tutup</button>
						      </div>
						    </div>
						  </div>
						</div>
					"""
		return format_html(modal_html)


	def save(self, *args, **kw):
		super(BeritaHukum, self).save(*args, **kw)
		url_handler_template(self.__class__.__name__, self.judul, self.pk)
