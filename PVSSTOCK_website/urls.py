"""PVSSTOCK_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from user import urls as user_urls
from search_device import urls as search_device_urls
from search_device.views import index, search_device


urlpatterns = [
    url('admin/', admin.site.urls),
    url(r"^$",search_device,name="search_device"),
    url(r"^index$",index,name="index"),
    url(r"^user/",include(user_urls,namespace="user")),
    url(r"^device/",include(search_device_urls)),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
