# Программа проверяет права по кадастровому номеру

import os
import random
import openpyxl
import time
from rosreestr_online import getCadNumApartment, getTypeObject, getObjectId, getRightReg

# wb = openpyxl.load_workbook('input_output_gettypeObjectFlat.xlsx')
# sheet = wb.active
# max_row = sheet.max_row

cadnum = "42:30:0302016:242"

objectId = getObjectId(cadnum)
print(objectId)
data = getRightReg(objectId)
print(data)



