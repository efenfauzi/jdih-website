#!/usr/bin/env python
import os, sys
import django
sys.path.append(os.getcwd())
os.environ["DJANGO_SETTINGS_MODULE"] = "jdih_web.settings"
django.setup()

from django.conf import settings
from module_admin_list.models import PermissionList

data_all = PermissionList.objects.all()
print(data_all)

for dt in data_all:
	if "can delete" in dt.name.lower():
		new_name = dt.name.lower().split("can delete")[-1]
		dt.name = "%s | Hapus" %new_name.title()
	if "can add" in dt.name.lower():
		new_name = dt.name.lower().split("can add")[-1]
		dt.name = "%s | Tambah" %new_name.title()
	if "can view" in dt.name.lower():
		new_name = dt.name.lower().split("can view")[-1]
		dt.name = "%s | Tampil" %new_name.title()
	if "can change" in dt.name.lower():
		new_name = dt.name.lower().split("can change")[-1]
		dt.name = "%s | Ubah" %new_name.title()
	dt.save()

