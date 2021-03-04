from django.db import models
from ckeditor.fields import RichTextField
from module_admin_list.models import UserJDIHCostum
# from django.contrib.auth.models import User as UserJDIHCostum
from django.utils.html import format_html
from jdih_libs.models_helpers import url_handler_template
from jdih_libs.utils import encode_string

# Create your models here.

class PengetahuanHukumPraktis(models.Model):
	judul = models.CharField(max_length=255, help_text='Isikan judul berita hukum',verbose_name='Judul')
	konten = RichTextField(verbose_name='Isi')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	created_by = models.ForeignKey(UserJDIHCostum, on_delete=models.CASCADE, editable=False)
	updated_by = models.ForeignKey(UserJDIHCostum, related_name='username_pengetahuan_hukum', on_delete=models.CASCADE, editable=False, null=True)


	def __str__(self):
		return self.judul

	class Meta:
		db_table = 'jdih_pengetahuan_hukum_praktis'
		verbose_name_plural = 'Pengetahuan Hukum Praktis'
		verbose_name = 'Pengetahuan Hukum Praktis'


	def riwayat_pengetahuan_hukum_praktis(self):
		created = (self.created_at).strftime("%d %B %Y jam %H:%M")
		if self.updated_by is None:
			update_on = '-'
		else:
			update_on = (self.updated_at).strftime("%d %B %Y jam %H:%M")
			update_on = f"<b>{self.updated_by}</b> pada {update_on}"

		return format_html(f"dibuat : <b>{self.created_by}</b> pada {created}</br>\
							diedit : {update_on}") 

	def preview_pengetahuan_hukum(self):
		rand_name = encode_string(self.judul) 
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
						        <h3 class="modal-title text-center" id="{self.id}-{rand_name}Title">{self.judul}</h3>
						        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
						          <span aria-hidden="true">&times;</span>
						        </button>
						      </div>
						      <div class="modal-body">
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
		super(PengetahuanHukumPraktis, self).save(*args, **kw)
		url_handler_template(self.__class__.__name__, self.judul, self.pk)
