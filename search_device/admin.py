from django.contrib import admin
from .models import ManageDevice

# Register your models here.


class AdminManageDevice(admin.ModelAdmin):
	model = ManageDevice
	list_display = ["id","brand","model","kind","quantity",]









admin.site.register(ManageDevice,AdminManageDevice)