from django.conf import settings
from django import template
from html import unescape
from django.utils.html import mark_safe, format_html
from jdih_libs.models_helpers import normalize_string_param
from datetime import datetime
# Depending on your django version, `reverse` and `NoReverseMatch` has been moved.
# From django 2.0 they've been moved to `django.urls`
try:
	from django.urls import reverse, NoReverseMatch
except ImportError:
	from django.core.urlresolvers import reverse, NoReverseMatch

register = template.Library()

# From django 1.9 `assignment_tag` is deprecated in favour of `simple_tag`
try:
	simple_tag = register.simple_tag
except AttributeError:
	simple_tag = register.assignment_tag

# importing models
from module_template.models import TemplateHeader, RunningTextHeader
from module_content_dinamis.models import KontenDinamis
from module_pranala_luar.models import PranalaLuar
from django.core.exceptions import ObjectDoesNotExist


def homepage_base(value):
	try:
		tmpl_web = TemplateHeader.objects.get(set_default=True)
		if value == 'logo':
			return tmpl_web.logo.url
		elif value == 'banner':
			return tmpl_web.banner.url
		elif value == 'alamat':
			return format_html(mark_safe(tmpl_web.address))
		elif value == 'footer':
			return mark_safe(unescape(tmpl_web.footer))
	except ObjectDoesNotExist:
		if value == 'logo':
			return f'{settings.STATIC_URL}web/img/logo-jdihn.png'
		elif value == 'banner':
			return f'{settings.STATIC_URL}web/img/banner-placeholder.png'
		elif value == 'alamat':
			return mark_safe("<p>Data alamat tidak tersedia</p>")
		elif value == 'footer':
			return mark_safe(unescape(f"<p>Copyright ©{datetime.now().year} Website Jaringan Dokumentasi dan Informasi</p>"))		

register.simple_tag(homepage_base)

def running_text(value):
	try:
		run_text = RunningTextHeader.objects.get(set_default=True)
		if value == 'arah_scroll':
			return run_text.arah_scroll
		if value == 'kecepatan_scroll':
			return run_text.kecepatan_scroll
		if value == 'text':
			return run_text.text
	except ObjectDoesNotExist:
		if value == 'arah_scroll':
			return "left"
		if value == 'kecepatan_scroll':
			return 3
		if value == 'text':
			return "data teks tidak tersedia, silahkan tambahkan data dan set default"
register.simple_tag(running_text)

def menu_list(context):
	konten_dinamis = KontenDinamis.objects.all().order_by('urutan_menu')[:4]
	request = context["request"]
	html = ''
	for menu_list in konten_dinamis:
		url = f'/halaman/{normalize_string_param(menu_list.menu)}'
		if url == request.path:
			current = 'active'
			span_current = '<span class="sr-only">(current)</span>'
		else:
			current = ''
			span_current = ''
		html += f"""<li class="nav-item {current}">
					  <a class="nav-link" href="{url}">{menu_list.menu}
						{span_current}
					  </a>
					</li>
				"""
	return format_html(html)
register.simple_tag(menu_list, takes_context=True)



def link_terkait():
	pranala_luar = PranalaLuar.objects.all().order_by('pk')[:8]
	print(pranala_luar)
	html = ''
	for link in pranala_luar:
		html += f"""
				<li>\
				 <a href="{link.url}" target="_blank">\
				  <span class="badge blue-theme-footer">\
				   - {link.title.upper()}\
				  </span>\
				 </a>\
			 	<li>\
				"""
	return format_html(html)
register.simple_tag(link_terkait)


@register.filter(name='url_name')
def url_name(value):
	return normalize_string_param(value)

@register.filter(name='sort_apps')
def sort_apps(apps):
	count = len(apps)
	apps.sort(key = lambda x: 
		settings.APP_ORDER.index(x['app_label'])
		if x['app_label'] in settings.APP_ORDER 
		else count
		)

	return apps