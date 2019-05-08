from django.conf.urls import url

from .views import import_data, search_device, edit_device, DeviceDelete, add_store, StoreDelete, request_quota





urlpatterns = [

	url(r"^upload-excel-file/$",import_data,name="import_data"),
	url(r"^search-device/$",search_device,name="search_device"),
	url(r"^edit-device/(?P<pk>\d+)/$",edit_device,name="edit_device"),
	url(r"^delete-device/(?P<pk>\d+)/$",DeviceDelete.as_view(),name="delete_device"),
	url(r"^add-store/$",add_store,name="add_store"),
	url(r"^delete-store/(?P<pk>\d+)/$",StoreDelete.as_view(),name="delete_store"),
	url(r"^request-quota/(?P<pk>\d+)/$",request_quota,name="request_quota"),	

]