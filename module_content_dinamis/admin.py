from django.contrib import admin
from module_content_dinamis.models import *

# Register your models here.
class KontenDinamisAdmin(admin.ModelAdmin):
	list_display = ('menu','urutan_menu')
	fieldsets = (
				('Konten Dinamis (*kolom cetak tebal wajib diisi)', {
					'fields': (('menu','urutan_menu'),'konten')
				}),
				)


admin.site.register(KontenDinamis, KontenDinamisAdmin)