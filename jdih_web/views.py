from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from html import unescape
from django.template import RequestContext

# import models
from module_berita_hukum.models import BeritaHukum
from module_template.models import SliderImage, URLModelResolve
from module_berita_hukum.models import BeritaHukum
from module_content_dinamis.models import KontenDinamis
from module_pengetahuan_hukum_praktis.models import PengetahuanHukumPraktis

# HTTP Not Found 404
def page_not_found(request, exception=None):
	return render(request, 'homepage/404.html', status=404)

# HTTP Not Found 404
def response_error_handler(request, exception=None):
	return render(request, 'homepage/500.html', status=500)

def homepage(request):
	berita_hukum = BeritaHukum.objects.all().order_by('pk')[:4]
	pengetahuan_hukum = PengetahuanHukumPraktis.objects.all().order_by('pk')[:5]

	image_slideshow = SliderImage.objects.all().order_by('urutan')

	return render(request, 'homepage/homepage.html', 
					{'berita_hukum': berita_hukum,
					 'image_slideshow': image_slideshow,
					 'pengetahuan_hukum': pengetahuan_hukum
					}
					)


def page_view(request, string_param):
	print(string_param)
	data = get_object_or_404(URLModelResolve, string_param=string_param)
	if data.model_name == 'KontenDinamis':
		data_list = KontenDinamis.objects.get(pk=data.id_param)
		title = data_list.menu
		konten = data_list.konten
		image_news = ''
	if data.model_name == 'BeritaHukum':
		data_list = BeritaHukum.objects.get(pk=data.id_param)
		title = data_list.judul
		konten = data_list.konten
		image_news = data_list.image
	if data.model_name == 'PengetahuanHukumPraktis':
		data_list = PengetahuanHukumPraktis.objects.get(pk=data.id_param)
		title = data_list.judul
		konten = data_list.konten
		image_news = ''
	return render(request, 'homepage/halaman_konten_all.html', 
					{'title': title,
					 'konten': konten,
					 'image_news': image_news
					}
					)
