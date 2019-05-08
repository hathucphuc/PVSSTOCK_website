from django.db import models
from django.urls import reverse
from user.models import User

# Create your models here.

class UploadExcel(models.Model):
	file_excel = models.FileField('Upload Excel File',upload_to="upload_excel/")

class Store(models.Model):
	name = models.CharField(max_length=30)
	address = models.CharField(max_length=100)
	user = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.name

	def get_delete_url(self):
		return reverse("delete_store",kwargs={"pk":self.pk})



class ManageDevice(models.Model):
	brand = models.CharField(max_length=20)
	model = models.CharField(max_length=30)
	kind = models.CharField(max_length=20)
	description = models.TextField()
	quantity = models.CharField(max_length=10)
	provider = models.CharField(max_length=20)
	phone = models.CharField(max_length=20)
	note = models.CharField(max_length=100,blank=True)
	public = models.BooleanField(default=True,help_text='Check box when you want public item.')
	store = models.ManyToManyField(Store,blank=True,related_name='stores')
	user = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return "{} {}".format(self.brand,self.model)

	def get_absolute_url(self):
		return reverse("request_quota",kwargs={"pk":self.pk})

	def get_update_url(self):
		return reverse("edit_device",kwargs={"pk":self.pk})

	def get_delete_url(self):
		return reverse("delete_device",kwargs={"pk":self.pk})

class RequestQuota(models.Model):
	device = models.ForeignKey(ManageDevice,on_delete=models.CASCADE,blank=True,null=True)
	company_name = models.CharField(max_length=50)
	phone = models.CharField(max_length=15)
	email = models.EmailField()
	quantity = models.CharField(max_length=10,blank=True,null=True)
	received_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.email



