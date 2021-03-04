from django.contrib import admin
from module_pengetahuan_hukum_praktis.models import *
# Register your models here.

class PengetahuanHukumPraktisAdmin(admin.ModelAdmin):
	list_display = 'judul', 'riwayat_pengetahuan_hukum_praktis', 'preview_pengetahuan_hukum'

	fieldsets = (
				('Pengetahuan Hukum Praktis (*kolom cetak tebal wajib diisi)', {
					'fields': ('judul', 'konten')
				}),
				)

	def save_model(self, request, obj, form, change):
		obj.created_by = request.user
		if change:
			obj.updated_by = request.user
		super().save_model(request, obj, form, change)

admin.site.register(PengetahuanHukumPraktis, PengetahuanHukumPraktisAdmin)