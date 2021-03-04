from django.contrib import admin
from module_non_peraturan.models import *
# Register your models here.


class DataListNonPeraturanAdmin(admin.ModelAdmin):
	list_display = 'subject', 'tanggal_posting', 'riwayat_data_peraturan'

	fieldsets = (
				('DATA NON PERATURAN (*kolom cetak tebal wajib diisi)', {
					'fields': ('subject', ('dokument','thumbnail'))
				}),
				('DATA ABSTRAK PERATURAN (*kolom cetak tebal wajib diisi)', {
					'classes': ('collapse', 'wide'),
					'fields': ('judul_buku',('authors','penerbit_buku'),\
								('kota_terbit','tahun_terbit'),\
								('col_number','jilid','jumlah_halaman'),\
								('tebal_buku','nomor_induk','status'),\
								'subject_pengarang_buku')
				}),
				)

admin.site.register(NonPeraturan, DataListNonPeraturanAdmin)
