"""jdih_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import jdih_web.views as jdih_web 
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf.urls import (handler400, handler403, handler404, handler500)


admin.site.site_header = 'JDIH Website Administration'                    		# default: "Django Administration"
admin.site.index_title = 'Control Panel Content'                 			# default: "Site administration"
admin.site.site_title = 'JDIH Website' 									# default: "Django site admin"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', jdih_web.homepage, name='homepage'),
    path('halaman/<str:string_param>', jdih_web.page_view, name='halaman_konten_all'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('favicon.ico',RedirectView.as_view(url='favicon.ico')),
]


if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = jdih_web.page_not_found
handler500 = jdih_web.response_error_handler

