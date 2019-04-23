from django.conf.urls import url

from .views import import_data, search_device, edit_device, DeviceDelete





urlpatterns = [

	url(r"^upload-excel-file/$",import_data,name="import_data"),
	url(r"^search-device/$",search_device,name="search_device"),
	url(r"^edit-device/(?P<pk>\d+)/$",edit_device,name="edit_device"),
	url(r"^delete-device/(?P<pk>\d+)/$",DeviceDelete.as_view(),name="delete_device"),
	

]