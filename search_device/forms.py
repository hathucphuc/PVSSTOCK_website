from django import forms

from django.core.exceptions import ValidationError

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

    

    def save(self,**kwargs):
        new = super().save(commit=False)
        user=self.user
        #new = ManageDevice.objects.create(brand=self.cleaned_data["brand"],model=self.cleaned_data["model"],description=self.cleaned_data["description"],kind=self.cleaned_data["kind"],quantity=self.cleaned_data["quantity"],provider=user.provider.name,phone=user.provider.phone,user=user)
        
        new.user = user
        new.provider = user.provider.name
        new.phone = user.provider.phone
        new.save()
        return new

class FilterForm(forms.Form):
	brand = forms.CharField(required=False)
	model = forms.CharField(required=False)
	kind = forms.CharField(required=False)
	description = forms.CharField(required=False)
	provider = forms.CharField(required=False)

	class Meta:
		fields = ["brand","model","description","kind","provider",]
