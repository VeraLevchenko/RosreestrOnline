import os
import random
import openpyxl
import time
from rosreestr_online import getCadNumApartment, getTypeObject


wb = openpyxl.load_workbook('Квартиры.xlsx')
sheet = wb.active
max_row = sheet.max_row




# type_street = 'улица'
# street = 'Франкфурта'
# house = 8
# apartment = 12
for i in range(637, max_row):
    type_street = sheet[i][1].value
    street = sheet[i][2].value
    house = sheet[i][3].value
    apartment = sheet[i][4].value
    cadnum = getCadNumApartment(type_street, street, house, apartment)
    print("cadnum", cadnum)
    if cadnum != "None":
        objectName = getTypeObject(cadnum)
    else:
        objectName = "None"
    print("", objectName)
    sheet[i][5].value = cadnum
    sheet[i][6].value = objectName
    wb.save('Квартиры.xlsx')

