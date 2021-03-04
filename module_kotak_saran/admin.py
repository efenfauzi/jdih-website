from django.contrib import admin
from module_kotak_saran.models import *
# Register your models here.

class KotakSaranAdmin(admin.ModelAdmin):
	list_display = ('nama_pengirim','email_pengirim','subyek','content','post_date')

admin.site.register(KotakSaran, KotakSaranAdmin)