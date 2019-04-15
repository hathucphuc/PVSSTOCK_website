from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
import xlrd, os
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import UploadForm, SearchDeviceForm
from .models import ManageDevice
#from .filters import DeviceFilter
# Create your views here.



def index(request):
	return render(request,"index.html",{})

@login_required
def import_data(request):
	if request.method == "POST":
		form = UploadForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()

			try:
				if ManageDevice.objects.filter(user=request.user):
					ManageDevice.objects.filter(user=request.user).delete()
			except:
				pass


			#path = "E:\\OneDrive\\Learning_Pyhton\\GITHUB\\PVSSTOCK_website\\media\\upload_excel\\%s" %(request.FILES["file_excel"].name)
			path = "/Users/haphuc/onedrive/Learning_Pyhton/GITHUB/PVSSTOCK_website/media/upload_excel/%s" %(request.FILES["file_excel"].name)

			workbook = xlrd.open_workbook(path)

			# number of sheets
			sheets = workbook.nsheets
			for s in range(sheets):

				# get sheets by index
				sheet = workbook.sheet_by_index(s)
				# number of rows and columns
				num_rows = sheet.nrows
				num_columns = sheet.ncols
				for r in range(1,num_rows):
					row = []
					for c in range(num_columns):
						row.append(sheet.cell(r,c).value)
					
					ManageDevice.objects.create(brand=row[0],model=row[1],kind=row[2],description=row[3],quantity=row[4],provider=request.user.provider.name,phone=request.user.provider.phone,user=request.user)
			os.remove(path)
			return redirect("search_device")
	else:
		form = UploadForm()
		return render(request,"search_device/upload_file_excel.html",{"form":form})

					
def search_device(request):
	if request.method == "POST":
		form_result = SearchDeviceForm(request.POST)
		if form_result.is_valid():
			devices = ManageDevice.objects.all()

			info = form_result.cleaned_data["search"]
			info = info.split()


			results = []
			for i in range(len(info)):
				result = ManageDevice.objects.filter(Q(brand__icontains=info[i]) | Q(model__icontains=info[i]) | Q(kind__icontains=info[i]) | Q(description__icontains=info[i]) |Q(provider__icontains=info[i]))
				result = list(result.values_list("brand","model","kind","description","quantity","provider","phone"))
				results = results + result
			results = list(set(results))
			

			form = SearchDeviceForm(initial={"search":form_result.cleaned_data["search"]})

			return render(request,"search_device/results.html",{"results":results,"form":form,"devices":devices})
	else:
		form = SearchDeviceForm()
		return render(request,"search_device/search_device.html",{"form":form})
