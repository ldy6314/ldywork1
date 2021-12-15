from openpyxl import Workbook

wb = Workbook()
ws1 = wb.create_sheet("Sheet1")
print(wb.sheetnames)
wb.save("test.xlsx")