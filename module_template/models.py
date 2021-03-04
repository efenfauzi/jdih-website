from django.db import models
from ckeditor.fields import RichTextField
from django.utils.html import format_html
from django.conf import settings
from PIL import Image


# Create your models here.
class TemplateHeader(models.Model):
	logo = models.ImageField(verbose_name="logo logo", help_text="Gambar dengan ukuran resolusi 90x120 \
							pixel atau dengan proposional yang serupa")
	banner = models.ImageField(verbose_name="banner header", help_text="Gambar dengan ukuran resolusi 640x120 \
							pixel atau dengan proposional yang serupa")
	footer = RichTextField(verbose_name="copyright")
	address = RichTextField(verbose_name="alamat")
	set_default = models.BooleanField(default=False, verbose_name="Tampil sebagai default")
	template_name = models.CharField(max_length=255, editable=False)

	def __str__(self):
		return "Template Web "+str(self.template_name)

	def save(self, *args, **kw):
		try:
			orig = TemplateHeader.objects.get(id=self.pk)
			if self.set_default:
				print("set default true on save")
				TemplateHeader.objects.filter(set_default=True).update(set_default=False)

		except self.DoesNotExist:
			count = TemplateHeader.objects.count()
			self.template_name = (count)+1
			if self.set_default:
				print("set default true on change")
				TemplateHeader.objects.filter(set_default=True).update(set_default=False)
		super(TemplateHeader, self).save(*args, **kw)

	def template_name_number(self):
		return f"Template Web {self.template_name}"

	class Meta:
		db_table = 'jdih_templates'
		verbose_name_plural = 'Template Beranda'
		verbose_name = 'Template Beranda'
		ordering = ['pk', 'template_name']

class RunningTextHeader(models.Model):
	text = models.CharField(max_length=250, help_text="text akan tampil berjalan \
		dengan bentuk marquee maksimal 250 Karakter")
	set_default = models.BooleanField(default=False, verbose_name="Tampil sebagai default")
	text_name = models.CharField(max_length=255, editable=False)
	list_arah = (('left', 'ke kiri'),('right', 'ke kanan'))
	arah_scroll = models.CharField(max_length=20, choices=list_arah, \
					default='left', help_text=format_html("arah scroll teks dari kiri ke kanan, atau</br>\
					dari kanan ke kiri"))  
	kecepatan_scroll = models.IntegerField(default=5, \
											help_text=format_html("kecepatan scroll \
														</br>1-10 : lambat\
														</br>11-20 : sedang\
														</br>21-30 : cepat\
														</br>30 keatas : sangat cepat")) 

	def __str__(self):
		return self.text_name

	def save(self, *args, **kw):
		try:
			orig = RunningTextHeader.objects.get(pk=self.pk)
			if self.set_default:
				print("set default true on save")
				RunningTextHeader.objects.filter(set_default=True).update(set_default=False)
		except self.DoesNotExist:
			count = RunningTextHeader.objects.count()
			self.text_name = f"Teks Berjalan {count+1}"
			if self.set_default:
				print("set default true on change")
				RunningTextHeader.objects.filter(set_default=True).update(set_default=False)
		super(RunningTextHeader, self).save(*args, **kw)

	def preview_text(self):

		html = f"""
					<marquee width="60%" behavior="scroll" direction="{self.arah_scroll}" \
					scrollamount="{self.kecepatan_scroll}" onmouseover="this.stop();" \
					onmouseout="this.start();">{self.text}</marquee>
				"""
		return format_html(html)

	class Meta:
		db_table = 'jdih_running_text'
		verbose_name_plural = 'Text Berjalan'
		verbose_name = 'Text Berjalan'
		ordering = ['pk',]



class SliderImage(models.Model):
	image = models.ImageField()
	image_name = models.CharField(max_length=250, editable=False)
	image_description = models.CharField(max_length=250,verbose_name="deskripsi", \
						help_text="Captions gambar\
						(contoh :  Lembaga Pemasyarakatan Hukum Kota...)")
	image_link = models.URLField(max_length=250, verbose_name="link",\
						help_text="Tambahkan link jika ada", null=True, blank=True)
	urutan = models.IntegerField()

	def __str__(self):
		return self.image_name

	def save(self, *args, **kw):
		try:
			orig = SliderImage.objects.get(pk=self.pk)
		except self.DoesNotExist:
			count = SliderImage.objects.count()
			self.image_name = f"Gambar Slideshow {count+1}"

		if self.image:
			img = Image.open(self.image)
			if img.height > 380 or img.width > 768:
				output_size = (768, 380)
				img.thumbnail = output_size
				img.save(self.image)

		super(SliderImage, self).save(*args, **kw)

	def preview_image(self):

		html = f"""
				<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#{self.pk}-modal-mage">
				  Preview
				</button>
				<div class="modal fade" id="{self.pk}-modal-mage" tabindex="-1" role="dialog" aria-labelledby="{self.pk}-imageModal" aria-hidden="true">
				  <div class="modal-dialog modal-dialog-centered" role="document">
				    <div class="modal-content">
				      <div class="modal-header">
				        <h5 class="modal-title" id="{self.pk}-modal-mage">{self.image_name}</h5>
				        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
				          <span aria-hidden="true">&times;</span>
				        </button>
				      </div>
				      <div class="modal-body">
				        <img src="{settings.MEDIA_URL}{self.image}" width="560px">
				      </div>
				      <div class="modal-footer">
				        <button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>
				      </div>
				    </div>
				  </div>
				</div>
				"""
		return format_html(html)

	class Meta:
		db_table = 'jdih_slide_image'
		verbose_name_plural = 'Slideshow Beranda'
		verbose_name = 'Slideshow Beranda'
		ordering = ['pk', 'image_name']


class URLModelResolve(models.Model):
	model_name = models.CharField(max_length=100)
	string_param = models.CharField(max_length=250)
	id_param = models.IntegerField()

	def __str__(self):
		return self.model_name

	class Meta:
		db_table = 'jdih_url_model_resolve'