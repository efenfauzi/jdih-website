from django.contrib import admin
from module_peraturan.models import *

# Register your models here.
class MenuKategoriPeraturan(admin.ModelAdmin):
	list_display = 'kelompok_menu', 'kategori_menu', 'urutan'
	fieldsets = (
				('DATA KATEGORI PERATURAN (*kolom cetak tebal wajib diisi)', {
					'fields': ('category_name',('parent','urutan'))
				}),
				)

class DataListPeraturanAdmin(admin.ModelAdmin):
	list_display = 'kategori', 'nomor_peraturan', 'subject', 'tanggal_posting', 'riwayat_data_peraturan'

	fieldsets = (
				('DATA PERATURAN (*kolom cetak tebal wajib diisi)', {
					'fields': ('subject',('kategori','status'),('tahun_peraturan','nomor_peraturan'),'dokument')
				}),
				('DATA KATALOG PERATURAN', {
					'classes': ('collapse',),
					'fields': (('catalog_tajuk_entri','catalog_judul_seragam'),('catalog_bentuk_nomor_tahun',\
						'catalog_tanggal_bulan_tahun'),('catalog_perihal','catalog_pengesahan','catalog_tahun_pengesahan'),\
						'catalog_sumber_teks','catalog_subject',('catalog_singkatan_peraturan','catalog_lokasi_penyimpanan'))
				}),
				('DATA ABSTRAK PERATURAN', {
				'classes': ('collapse',),
					'fields': (('abstract_subject','abstract_singkatan_peraturan'),('abstract_tahun','abstract_nomor'),\
								('abstract_sumber','abstract_jumlah_halaman','abstract_jenis'),'abstract_tentang',\
								'abstract_deskripsi','abstract_dasar_hukum','abstract_diatur','abstract_catatan',)
				}),
				)


admin.site.register(KategoriPeraturan, MenuKategoriPeraturan)
admin.site.register(DataListPeraturan, DataListPeraturanAdmin)


