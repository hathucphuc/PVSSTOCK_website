from django.conf.urls import url

from .views import import_data, search_device





urlpatterns = [

	url(r"^upload-excel-file/$",import_data,name="import_data"),
	url(r"^search-device/$",search_device,name="search_device"),
	

]