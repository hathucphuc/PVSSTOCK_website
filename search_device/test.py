import xlrd
from django.shortcuts import get_object_or_404
'''

path = "/Users/haphuc/onedrive/Learning_Pyhton/GITHUB/PVSSTOCK_website/media/upload_excel/%s" %("test_file.xlsx")

workbook = xlrd.open_workbook(path)

num_sheets = workbook.nsheets

for s in range(num_sheets):
	print(s)
	sheet = workbook.sheet_by_index(s)
	num_rows = sheet.nrows
	num_columns = sheet.ncols
	for r in range(1,num_rows):
		row = []
		for c in range(num_columns):
			row.append(sheet.cell(r,c).value)

		for r in range(len(row)):
			print(row[r])

'''
a = [1,2,3,3,3,4]
b = set(a)
for i in b:
	print(i)
c = "ha thuc phuc"
c = c.split()
print(c)