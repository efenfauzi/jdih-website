from module_template.models import URLModelResolve
from django.core.exceptions import ObjectDoesNotExist


def normalize_string_param(string_param):
	return string_param.lower().replace(" ", "-")

def url_handler_template(model_name, string_param, id_param):
	try:
		orig = URLModelResolve.objects.get(model_name=model_name, id_param=id_param)
		if normalize_string_param(orig.string_param) != normalize_string_param(string_param):
			orig.string_param = normalize_string_param(string_param)
			orig.save()
	except ObjectDoesNotExist:
		data = URLModelResolve(string_param=normalize_string_param(string_param), id_param=id_param, 
								model_name= model_name)
		data.save()