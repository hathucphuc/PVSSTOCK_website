from django.contrib import admin
from .models import ManageDevice, Store

# Register your models here.


class AdminManageDevice(admin.ModelAdmin):
	model = ManageDevice
	list_display = ["id","brand","model","kind","quantity",]


class AdminStore(admin.ModelAdmin):
	model = Store
	list_display = ["id","name","user"]





admin.site.register(ManageDevice,AdminManageDevice)
admin.site.register(Store,AdminStore)