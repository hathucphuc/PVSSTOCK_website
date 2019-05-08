from django import forms
from django.http import HttpResponse

from django.core.exceptions import ValidationError, FieldError, ObjectDoesNotExist

from .models import UploadExcel, ManageDevice, Store, RequestQuota








class UploadForm(forms.Form):
	file_excel = forms.FileField()
	public = forms.BooleanField(help_text='Uncheckbox when you dont want public your devices.')

	class Meta:
		fields = ["file_excel","store","public"]

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user',None)
		super(UploadForm, self).__init__(*args, **kwargs)
		self.fields["store"] = forms.ModelMultipleChoiceField(queryset=Store.objects.filter(user=self.user),widget=forms.CheckboxSelectMultiple, required=False, help_text='Choose stores which you want store your devices.')
		self.fields["public"].required=False

	def clean_file_excel(self):
		#cleaned_data = super().clean()
		file_excel = self.cleaned_data.get("file_excel")
		if file_excel:
			if file_excel.name.endswith((".xls",".xlsx")):
				print("excel")
				return file_excel
			else:
				raise ValidationError("The File is not a excel file. Please upload only excel file.")

class SearchDeviceForm(forms.Form):
	search = forms.CharField()

	class Meta:
		fields = ["search"]


class AddDeviceForm(forms.ModelForm):

	class Meta:
		model = ManageDevice
		fields = ["brand","model","description","public","kind","quantity","store"]
		#widgets = {
           # 'store': forms.CheckboxSelectMultiple,}

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user',None)
		super(AddDeviceForm, self).__init__(*args, **kwargs)
		self.fields["store"] = forms.ModelMultipleChoiceField(queryset=Store.objects.filter(user=self.user),widget=forms.CheckboxSelectMultiple, required=False)
		self.fields["public"].required=False


	#store = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Store.objects.filter(user=self.user))

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
		print("prepair")
		for store in self.cleaned_data["store"]:
			print("good!!!")
			new.store.add(store)
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


class AddStoreForm(forms.ModelForm):

	class Meta:
		model = Store
		fields = ["name","address"]
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user',None)
		super(AddStoreForm, self).__init__(*args, **kwargs)

	def clean_name(self):
		name = self.cleaned_data["name"]
		
		user = self.user
		
		try:
			Store.objects.get(name=name,user=user)		
			raise ValidationError("This name already exists.")
		except(FieldError, ValueError, ObjectDoesNotExist):
			
			return name

class RequestQuotaForm(forms.ModelForm):

	
	class Meta:
		model = RequestQuota
		fields = ["company_name","phone","email","quantity"]

		



