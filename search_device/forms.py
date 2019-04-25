from django import forms
from django.http import HttpResponse

from django.core.exceptions import ValidationError, FieldError, ObjectDoesNotExist

from .models import UploadExcel, ManageDevice








class UploadForm(forms.ModelForm):
	
	class Meta:
		model = UploadExcel
		fields = ["file_excel"]

	def clean_file_excel(self):
		#cleaned_data = super().clean()
		file_excel = self.cleaned_data.get("file_excel")
		if file_excel:
			if file_excel.name.endswith((".xls",".xlsx")):
				return file_excel
			else:
				raise ValidationError("The File is not a excel file. Please upload only excel file.")

class SearchDeviceForm(forms.Form):
	search = forms.CharField()

	class Meta:
		fields = ["search"]


class AddDeviceForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user',None)
		super(AddDeviceForm, self).__init__(*args, **kwargs)

	class Meta:
		model = ManageDevice
		fields = ["brand","model","description","kind","quantity",]

	def clean_model(self):
		model = self.cleaned_data["model"].upper()
		
		user = self.user
		
		try:
			ManageDevice.objects.get(model=model,user=user)		
			raise ValidationError("A device with model already exists.")
		except(FieldError, ValueError, ObjectDoesNotExist):
			
			return model
    	

	def save(self,**kwargs):
		new = super().save(commit=False)
		user=self.user
	    
		new.user = user
		new.provider = user.provider.name
		new.phone = user.provider.phone
		new.save()
		print("save")
		return new

class EditDeviceForm(AddDeviceForm):
	def __init__(self, *args, **kwargs):
		self.pk = kwargs.pop('pk',None)
		super(EditDeviceForm, self).__init__(*args, **kwargs)

	def clean_model(self):
		model = self.cleaned_data["model"].upper()
		pk = self.pk
		user = self.user
		device = ManageDevice.objects.get(pk=pk)
		if device.model == model:
			return model
		else:
			try:
				ManageDevice.objects.get(user=user,model=model)
				raise ValidationError("A device with model already exists.")
			except(FieldError, ValueError, ObjectDoesNotExist):
			
				return model

class FilterForm(forms.Form):
	brand = forms.CharField(required=False)
	model = forms.CharField(required=False)
	kind = forms.CharField(required=False)
	description = forms.CharField(required=False)
	provider = forms.CharField(required=False)

	class Meta:
		fields = ["brand","model","description","kind","provider",]
