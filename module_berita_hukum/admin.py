from django.contrib import admin
from module_berita_hukum.models import *
# Register your models here.

class BeritaHukumAdmin(admin.ModelAdmin):
	list_display = 'judul', 'riwayat_berita_hukum', 'preview_berita'

	fieldsets = (
				('BERITA HUKUM (*kolom cetak tebal wajib diisi)', {
					'fields': ('judul', 'konten','image')
				}),
				)

	def save_model(self, request, obj, form, change):
		obj.created_by = request.user
		if change:
			obj.updated_by = request.user
		super().save_model(request, obj, form, change)


admin.site.register(BeritaHukum, BeritaHukumAdmin)
