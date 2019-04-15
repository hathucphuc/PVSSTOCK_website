from django.contrib import admin

from django.contrib.admin import ModelAdmin
from django.contrib.auth.forms import UserCreationForm
from .forms import ProviderSignUpForm
from .models import User, Provider
# Register your models here.


class CustomUserAdmin(ModelAdmin):

	list_display = ["email","is_staff","is_active","is_provider"]
	model = User
	ordering = ["email",]

class ProviderAdmin(ModelAdmin):
	model = Provider
	list_display = ["user","name","phone"]
	ordering = ["name",]


admin.site.register(User,CustomUserAdmin)
admin.site.register(Provider,ProviderAdmin)
