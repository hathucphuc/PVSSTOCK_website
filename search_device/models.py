from django.db import models
from user.models import User

# Create your models here.

class UploadExcel(models.Model):
	file_excel = models.FileField('Upload Excel File',upload_to="upload_excel/")


class ManageDevice(models.Model):
	brand = models.CharField(max_length=20)
	model = models.CharField(max_length=30)
	kind = models.CharField(max_length=20)
	description = models.TextField()
	quantity = models.CharField(max_length=10)
	provider = models.CharField(max_length=20)
	phone = models.CharField(max_length=20)
	user = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return "{} {}".format(self.brand,self.model)