from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
import xlrd, os, re, openpyxl
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core.mail import EmailMessage, send_mail, get_connection
from django.template.loader import get_template

from .forms import UploadForm, SearchDeviceForm, AddDeviceForm, FilterForm, EditDeviceForm, AddStoreForm, RequestQuotaForm
from .models import ManageDevice, Store, UploadExcel, RequestQuota
from .utils import get_price, get_dup_list, get_hightest_price, final_list
#from .filters import DeviceFilter
# Create your views here.



def index(request):
	return render(request,"index.html",{})

@login_required
def import_data(request):
	if request.method == "POST":
		form = UploadForm(request.POST,request.FILES,user=request.user)
		if form.is_valid():
			file = UploadExcel(file_excel=request.FILES['file_excel'])
			file.save()

			status = form.cleaned_data["public"]
			stores = form.cleaned_data["store"]

			file_name = request.FILES["file_excel"].name.replace(" ","_")
			file_name = re.sub(r"[\(\)\<\>\{\}]+","",file_name)

			# path = "E:\\OneDrive\\Learning_Pyhton\\GITHUB\\PVSSTOCK_website\\media\\upload_excel\\%s" %(file_name)
			# path = "/Users/haphuc/onedrive/Learning_Pyhton/GITHUB/PVSSTOCK_website/media/upload_excel/%s" %(file_name)
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
					price = get_price(row[5])
					try:
						device = ManageDevice.objects.get(model=model,user=request.user)
						for store in device.store.all():
							device.store.remove(store)
						for store in stores:
							device.store.add(store)
						device.public = status
						device.quantity = int(row[4])
						device.price = price
						device.save()
						
					except:
						device=ManageDevice.objects.create(brand=row[0],model=model,kind=row[2],description=row[3],quantity=int(row[4]),price=price,provider=request.user.provider.name,phone=request.user.provider.phone,user=request.user)
						for store in stores:
							device.store.add(store)
						
			os.remove(path)
			
			return redirect("user:profile")

		return render(request,"search_device/upload_file_excel.html",{"form":form})
	else:
		form = UploadForm(user=request.user,initial={"public":True,})
		return render(request,"search_device/upload_file_excel.html",{"form":form})

					
def search_device(request):
	devices = ManageDevice.objects.all()
		
	if request.method == "POST":
		form_result = SearchDeviceForm(request.POST)
		form_filter = FilterForm(request.POST)
		if form_result.is_valid():
			

			info = form_result.cleaned_data["search"]
			info = info.split()


			results = ManageDevice.objects.none()
			#results = []
			for i in range(len(info)):
				result = ManageDevice.objects.filter(Q(brand__icontains=info[i]) | Q(model__icontains=info[i]) | Q(kind__icontains=info[i]) | Q(description__icontains=info[i]))

				# results = results.union(result)
				results |= result
		
			# get hightest price object and delete lower price objects, duplicate objects
			results = final_list(results,ManageDevice)
			

			form = SearchDeviceForm(initial={"search":form_result.cleaned_data["search"]})
			form_filter = FilterForm()
		
			return render(request,"search_device/results.html",{"results":results,"form":form,"form_filter":form_filter})

		elif form_filter.is_valid():
			brand = form_filter.cleaned_data["brand"]
			model = form_filter.cleaned_data["model"]
			kind = form_filter.cleaned_data["kind"]
			description = form_filter.cleaned_data["description"]
			# provider = form_filter.cleaned_data["provider"]

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

			# if provider:
			# 	provider_set = ManageDevice.objects.filter(provider__icontains=provider)
			# else:
			# 	provider_set = ManageDevice.objects.all()


			# results = brand_set.intersection(model_set).intersection(kind_set).intersection(description_set)
			results = brand_set & model_set & kind_set & description_set
			# get hightest price object and delete lower price object
			results = final_list(results,ManageDevice)
			
			form_filter=FilterForm(initial={"brand":brand,"model":model,"description":description,"kind":kind})
			form = SearchDeviceForm()
			return render(request,"search_device/filter_device.html",{"results":results,"form_filter":form_filter,"form":form})
		
	else:
		form = SearchDeviceForm()
		return render(request,"search_device/search_device.html",{"form":form,})

@login_required
def edit_device(request,pk):
	device = ManageDevice.objects.get(pk=pk)
	if request.method == "POST":
		form = EditDeviceForm(request.POST,user=request.user,pk=pk)
		if form.is_valid():

			device.brand = form.cleaned_data["brand"]
			device.model = form.cleaned_data["model"]
			device.kind = form.cleaned_data["kind"]
			device.description = form.cleaned_data["description"]
			device.public = form.cleaned_data["public"]
			device.quantity = form.cleaned_data["quantity"]
			device.price = get_price(form.cleaned_data["price"])
			device.note = form.cleaned_data["note"]
			device.save()

			for store in device.store.all():
				device.store.remove(store)

			stores = form.cleaned_data["store"]
			for store in stores:
				#st = Store.objects.get(user=request.user,name=store["name"])
				device.store.add(store)
			return redirect("user:profile")

	else:

		form = EditDeviceForm(initial={"brand":device.brand,"model":device.model,"description":device.description,"public":device.public,"kind":device.kind,"quantity":device.quantity,"price":device.price,"note":device.note,"store":[d.pk for d in device.store.all()]},user=request.user)
	return render(request,"search_device/edit_device.html",{"form":form,"device":device})



class DeviceDelete(DeleteView):
	model = ManageDevice
	success_url = reverse_lazy("user:profile")
	template_name = "search_device/delete_device.html"

@login_required
def add_store(request):
	if request.method == "POST":
		form = AddStoreForm(request.POST,user=request.user)
		if form.is_valid():
			form=form.save(commit=False)
			form.user = request.user
			form.save()
			return redirect("user:profile")
		return HttpResponse("<h1 style='text-align:center;'>Add store failed!</h1>")

class StoreDelete(DeleteView):
	model = Store
	success_url = reverse_lazy("user:profile")
	template_name = "search_device/delete_store.html"

def request_quota(request,pk):
	device = ManageDevice.objects.get(pk=pk)

	# get all devices have same model
	list_device=ManageDevice.objects.filter(model=device.model)
	if request.method == "POST":
		print("post")
		form = RequestQuotaForm(request.POST)
		if form.is_valid():
			
			form = form.save(commit=False)

			# convert price to int
			price = int(re.sub(r",","",device.price))
			quantity = int(re.sub(r",","",form.quantity))
			total_price = price*quantity

			form.device = device.model
			form.price_quote = get_price(total_price)
			form.save()

			## input user infomation to contract ##
			path_model_quote = "/home/django_pvsstock/PVSSTOCK_website/media/file_contract/Quote_Device_PVStock_Eng.xlsx"
			# path_model_quote = "E:\\OneDrive\\Learning_Pyhton\\GITHUB\\PVSSTOCK_website\\media\\file_contract\\Quote_Device_PVStock_Eng.xlsx"
			# path_model_quote = "/Users/haphuc/onedrive/Learning_Pyhton/GITHUB/PVSSTOCK_website/media/file_contract/Quote_Device_PVStock_Eng.xlsx"
			quote = openpyxl.load_workbook(path_model_quote)
			# select currently sheet
			sheet = quote.active
			# input values to file quote
			sheet["E11"] = form.company_name
			sheet["E12"] = form.phone
			sheet["E13"] = form.email
			sheet["H11"] = form.id

			# sheet.unmerge_cells(start_row=18, start_column=3, end_row=18, end_column=4)
			sheet.unmerge_cells("D18:E18")
			sheet.cell(18,4).value = device.model
			# sheet.merge_cells(start_row=18, start_column=3, end_row=18, end_column=4)
			sheet.merge_cells("D18:E18")
			sheet["F18"] = price
			sheet["G18"] = quantity
			

			# save file quote to path_quote
			path_quote = "/home/django_pvsstock/PVSSTOCK_website/media/file_contract/Quote_Device_PVStock_customer.xlsx"
			# path_quote = "E:\\OneDrive\\Learning_Pyhton\\GITHUB\\PVSSTOCK_website\\media\\file_contract\\Quote_Device_PVStock_customer.xlsx"
			# path_quote = "/Users/haphuc/onedrive/Learning_Pyhton/GITHUB/PVSSTOCK_website/media/file_contract/Quote_Device_PVStock_customer.xlsx"
			quote.save(filename=path_quote)

			# send email
			subject1 = "pvstock.vn Ordering ID "+str(form.id)
			subject = "pvstock.vn customer request ordering ID "+str(form.id)
			from_email = "tech@pvs.com.vn"
			html_message = get_template("search_device/email_to_pvs.txt").render({"form":form,"list_device":list_device,"device":device})
			html_message1 = get_template("search_device/email_to_user.txt").render({"form":form,"device":device})

			msg = EmailMessage(subject,html_message,from_email,to=["sale@pvs.com.vn",])
			msg.content_type = "html"
			msg1 = EmailMessage(subject1,html_message1,from_email,to=[form.email,],cc=["sale@pvs.com.vn",])
			msg1.content_type = "html"

			msg1.attach_file(path_quote)
			msg.send()
			msg1.send()

			os.remove(path_quote)
			return HttpResponse("<h1 style='text-align:center;'>Your request quotation is send successfully!</h1>")
		return render(request,"search_device/request_quota.html",{"form":form,"device":device,})
	else:
		form = RequestQuotaForm()
		return render(request,"search_device/request_quota.html",{"form":form,"device":device,})
@login_required
def edit_ticket(request,pk):
	ticket = RequestQuota.objects.get(pk=pk)
	if request.method == "POST":
		form = RequestQuotaForm(request.POST)
		if form.is_valid():

			ticket.company_name = form.cleaned_data["company_name"]
			ticket.email = form.cleaned_data["email"]
			ticket.phone = form.cleaned_data["phone"]
			ticket.quantity = form.cleaned_data["quantity"]
			ticket.price_quote = get_price(form.cleaned_data["price_quote"])
			
			ticket.save()

			return redirect("user:profile")

	else:

		form = RequestQuotaForm(initial={"company_name":ticket.company_name,"email":ticket.email,"phone":ticket.phone,"quantity":ticket.quantity,"price_quote":ticket.price_quote})
	return render(request,"search_device/edit_ticket.html",{"form":form,"ticket":ticket})