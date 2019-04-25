from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
import xlrd, os, re
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse

from .forms import UploadForm, SearchDeviceForm, AddDeviceForm, FilterForm, EditDeviceForm
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

			file_name = request.FILES["file_excel"].name.replace(" ","_")
			file_name = re.sub(r"[\(\)\<\>\{\}]+","",file_name)

			#path = "E:\\OneDrive\\Learning_Pyhton\\GITHUB\\PVSSTOCK_website\\media\\upload_excel\\%s" %(file_name)
			#path = "/Users/haphuc/onedrive/Learning_Pyhton/GITHUB/PVSSTOCK_website/media/upload_excel/%s" %(file_name)
			path = "/home/django_pvsstock/PVSSTOCK_website/media/upload_excel/%s" %(file_name)

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
					if type(row[1])==str:
						model = row[1].upper()
					else:
						model = int(row[1])
					if type(row[4])==str or row[4]==0 or row[4]=="":
						continue
					try:
						device = ManageDevice.objects.get(model=model,user=request.user)
						device.quantity = int(row[4])
						device.save()
						print("successfully")

						
					except:
						ManageDevice.objects.create(brand=row[0],model=model,kind=row[2],description=row[3],quantity=int(row[4]),provider=request.user.provider.name,phone=request.user.provider.phone,user=request.user)
						
			os.remove(path)
			
			return redirect("user:profile")
	else:
		form = UploadForm()
		return render(request,"search_device/upload_file_excel.html",{"form":form})

					
def search_device(request):
	devices = ManageDevice.objects.all()
	

	
	if request.method == "POST":
		form_result = SearchDeviceForm(request.POST)
		form_filter = FilterForm(request.POST)
		if form_result.is_valid():
			

			info = form_result.cleaned_data["search"]
			info = info.split()


			results = []
			for i in range(len(info)):
				result = ManageDevice.objects.filter(Q(brand__icontains=info[i]) | Q(model__icontains=info[i]) | Q(kind__icontains=info[i]) | Q(description__icontains=info[i]) |Q(provider__icontains=info[i]))
				result = list(result.values_list("brand","model","kind","description","quantity","provider","phone"))
				results = results + result
			results = list(set(results))
			

			form = SearchDeviceForm(initial={"search":form_result.cleaned_data["search"]})
			form_filter = FilterForm()

			return render(request,"search_device/results.html",{"results":results,"form":form,"form_filter":form_filter,"devices":devices})

		elif form_filter.is_valid():
			brand = form_filter.cleaned_data["brand"]
			model = form_filter.cleaned_data["model"]
			kind = form_filter.cleaned_data["kind"]
			description = form_filter.cleaned_data["description"]
			provider = form_filter.cleaned_data["provider"]

			if brand:
				brand_set = ManageDevice.objects.filter(brand__icontains=brand)
			else:
				brand_set = ManageDevice.objects.all()
			if model:
				model_set = ManageDevice.objects.filter(model__icontains=model)
			else:
				model_set = ManageDevice.objects.all()
			if kind:
				kind_set = ManageDevice.objects.filter(kind__icontains=kind)
			else:
				kind_set = ManageDevice.objects.all()
			if description:
				description_set = ManageDevice.objects.filter(description__icontains=description)
			else:
				description_set = ManageDevice.objects.all()

			if provider:
				provider_set = ManageDevice.objects.filter(provider__icontains=provider)
			else:
				provider_set = ManageDevice.objects.all()

			brand_set = set(list(brand_set.values_list("brand","model","kind","description","quantity","provider","phone")))
			model_set = set(list(model_set.values_list("brand","model","kind","description","quantity","provider","phone")))
			kind_set = set(list(kind_set.values_list("brand","model","kind","description","quantity","provider","phone")))
			description_set = set(list(description_set.values_list("brand","model","kind","description","quantity","provider","phone")))
			provider_set = set(list(provider_set.values_list("brand","model","kind","description","quantity","provider","phone")))

			set_all = brand_set.intersection(model_set).intersection(kind_set).intersection(description_set).intersection(provider_set)
			results = list(set_all)

			
			form_filter=FilterForm(initial={"brand":brand,"model":model,"description":description,"kind":kind, "provider":provider})
			form = SearchDeviceForm()
			return render(request,"search_device/filter_device.html",{"results":results,"form_filter":form_filter,"form":form})
		
	else:
		form = SearchDeviceForm()
		return render(request,"search_device/search_device.html",{"form":form,})


def edit_device(request,pk):
	device = ManageDevice.objects.get(pk=pk)
	if request.method == "POST":
		form = EditDeviceForm(request.POST,user=request.user,pk=pk)
		if form.is_valid():

			device.brand = form.cleaned_data["brand"]
			device.model = form.cleaned_data["model"]
			device.kind = form.cleaned_data["kind"]
			device.description = form.cleaned_data["description"]
			device.quantity = form.cleaned_data["quantity"]
			device.save()
			return redirect("user:profile")

	else:

		form = EditDeviceForm(initial={"brand":device.brand,"model":device.model,"description":device.description,"kind":device.kind,"quantity":device.quantity})
	return render(request,"search_device/edit_device.html",{"form":form,"device":device})

class DeviceDelete(DeleteView):
	model = ManageDevice
	success_url = reverse_lazy("user:profile")
	template_name = "search_device/delete_device.html"
	