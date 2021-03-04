from django.contrib import admin
from module_pranala_luar.models import *
# Register your models here.

class PranalaLuarAdmin(admin.ModelAdmin):
	list_display = ('title', 'url', 'urutan')

	fieldsets = (
				('Pranala Luar (*kolom cetak tebal wajib diisi)', {
					'fields': ('url', ('title','urutan'))
				}),
				)

admin.site.register(PranalaLuar, PranalaLuarAdmin)