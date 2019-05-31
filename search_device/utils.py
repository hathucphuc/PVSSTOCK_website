import re
from django.db.models import Count



# function get price

def get_price(price_given):
	price_given = str(price_given)
	price = "".join(re.findall(r"\d+",price_given))
	if price:
		if int(price) == 0:
			return "0"
		else:	
			price = "{:,}".format(int(price))
			return price
	else:
		return "0"


# find duplicate elements from list

def get_dup_list(my_list):
	dup_list = []
	for i in range(len(my_list)):
		if my_list.count(my_list[i])>1:
			dup_list.append(my_list[i])
	return dup_list

#  find hightest price

def get_hightest_price(prices):
	prices_int = []
	for p in prices:
		if p!="":
			price = int(re.sub(r",","",p))
			
		else:
			price = 0
		prices_int.append(price)
	hightest = max(prices_int)
	print(hightest)
	return hightest

def get_total_quantity(dup_devices):
	total = 0
	for d in dup_devices:
		total += int(d.quantity)
	return total

# get hightest price object and delete lower price object
def final_list(results,ManageDevice):
	#  set all devices comparison to Fasle
	devices_comparison = results.filter(comparison=True)
	if devices_comparison:
		for d in devices_comparison:
			d.comparison=False
			d.quantity_total = "0"
			d.save()
	# convert queryset to list
	# list_results = list(results.values_list("model",flat=True))

	duplicates = results.values("model").annotate(kind_count=Count("model")).filter(kind_count__gt=1)

	# get duplicate devices have same Model
	# list_dup_device = get_dup_list(list_results)
	# print("4")
	if duplicates:
		for duplicate_objects in duplicates:
			# delete duplicate device from results
			results = results.exclude(model=duplicate_objects["model"])

			# create queryest with duplicate devices
			dup_device = ManageDevice.objects.filter(model=duplicate_objects["model"])

			# get prices from the devices duplicate
			prices = list(dup_device.values_list("price",flat=True))
		
			# get hightest price
			hightest_price = get_hightest_price(prices)

			# get device has hightest price
			hightest_price_device = ManageDevice.objects.filter(model=duplicate_objects["model"],price=get_price(hightest_price)).first()
			# set comparison to True and put quantity to quantity_total on hightest_price_device
			# for d in hightest_price_device:
			# 	d.comparison = True
			# 	d.quantity_total = get_total_quantity(dup_device)
			# 	d.save()
			hightest_price_device.comparison = True
			hightest_price_device.quantity_total = get_total_quantity(dup_device)
			hightest_price_device.save()
			print(hightest_price_device)

			# add the devices have hightest price to results again
			results |= ManageDevice.objects.filter(pk=hightest_price_device.pk)
		return results
	else:
		return results



