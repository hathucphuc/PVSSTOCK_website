from django.contrib import admin
from .models import ManageDevice, Store, FileContract, RequestQuota

# Register your models here.


class AdminManageDevice(admin.ModelAdmin):
	model = ManageDevice
	list_display = ["id","brand","model","kind","quantity",]


class AdminStore(admin.ModelAdmin):
	model = Store
	list_display = ["id","name","user"]

class AdminFileContract(admin.ModelAdmin):
	model = FileContract
	list_display = ["id","name"]
class AdminRequestQuota(admin.ModelAdmin):
	model = RequestQuota
	list_display = ["id","email","phone","device"]



admin.site.register(ManageDevice,AdminManageDevice)
admin.site.register(Store,AdminStore)
admin.site.register(FileContract,AdminFileContract)
admin.site.register(RequestQuota,AdminRequestQuota)