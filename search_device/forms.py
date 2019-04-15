from django import forms

from django.core.exceptions import ValidationError

from .models import UploadExcel








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