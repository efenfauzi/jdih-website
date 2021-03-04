from django.contrib import admin
from module_template.models import *

# Register your models here.

class TemplateHeaderAdmin(admin.ModelAdmin):
	list_display = ('template_name_number','set_default')

class RunningTextHeaderAdmin(admin.ModelAdmin):
	list_display = ('text_name', 'set_default', 'preview_text')
	fieldsets = (
				('Teks Berjalan', {
					'fields': ('text', \
								('arah_scroll','kecepatan_scroll'),
								'set_default')
				}),
				)

class SliderImageAdmin(admin.ModelAdmin):
	list_display = ('image_name', 'image_description', 'image_link', 'urutan', 'preview_image')
	fieldsets = (
				('Slider Image Beranda', {
					'fields': (('image_description','image_link'), \
								('urutan','image'))
				}),
				)

class URLModelResolveAdmin(admin.ModelAdmin):
	list_display = ('model_name', 'string_param', 'id_param')

admin.site.register(TemplateHeader, TemplateHeaderAdmin)
admin.site.register(RunningTextHeader, RunningTextHeaderAdmin)
admin.site.register(SliderImage, SliderImageAdmin)
# admin.site.register(URLModelResolve, URLModelResolveAdmin)