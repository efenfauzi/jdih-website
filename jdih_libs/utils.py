# utils functions
import random
import uuid
import hashlib 

from datetime import datetime
from django.conf import settings

def get_filename(filename, request):
	filename = str(uuid.uuid4())
	return filename.upper()

def get_random_badges():
	list_badges = ['badge-primary',
					'badge-secondary',
					'badge-success',
					'badge-danger',
					'badge-warning',
					'badge-info',
					'badge-dark',
					]
	return random.choice(list_badges)


def list_tahun():
	list_tahun = []
	for r in range(settings.START_YEAR, (datetime.now().year+1)):
		list_tahun.append((r,r))
	return list_tahun

def encode_string(string_value):
	return hashlib.md5(string_value.encode()).hexdigest() 



