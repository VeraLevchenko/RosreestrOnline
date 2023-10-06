# Программа дописывает в файл тип объекта. Нужно для определения квартира или нежилое помещение

import os
import random
import openpyxl
import time
from rosreestr_online import getCadNumApartment, getTypeObject


wb = openpyxl.load_workbook('input_output_gettypeObjectFlat.xlsx')
sheet = wb.active
max_row = sheet.max_row

# type_street = 'улица'
# street = 'Франкфурта'
# house = 8
# apartment = 12
for i in range(2, 7):
    type_street = sheet[i][1].value
    street = sheet[i][2].value
    house = sheet[i][3].value
    apartment = sheet[i][4].value
    print(apartment)
    cadnum = getCadNumApartment(type_street, street, house, apartment)
    print("cadnum", cadnum)
    if cadnum != "None":
        objectName = getTypeObject(cadnum)
    else:
        objectName = "Нет помещения с таким адресом или адрес не полный"
    print("", objectName)
    sheet[i][5].value = cadnum
    sheet[i][6].value = objectName
    wb.save('input_output_gettypeObjectFlat.xlsx')


