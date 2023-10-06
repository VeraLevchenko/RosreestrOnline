# Программа содержит необходимые модули и тестово делает один запрос по адресу (на здание или участок по выбору)


import requests

headers = {"User-Agent": "Mozilla / 5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, как Gecko) Chrome/ 49.0.2623.110 YaBrowser / 16.4.1.8564 Safari/537.36",
		   'Content-Type': 'application/json',
		   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


# возвращает тип улицы без точки, в нижнем регистре, в полном формате (напр. "Ул." превратится в "улица")
def normalizationTypeStreet(type_street):
	type_ulicas = ["ул", "улица", "у", ]
	type_proezd = ["проезд", "пр-д", "проспект", "пр-т", "п-кт"]
	type_pereulok = ["пер", "пер-к", "переулок", "пр-т", "п-кт"]

	type_street = type_street.replace(".", '')
	type_street = type_street.lower()
	if type_street in type_ulicas:
		type_street = "улица"
	if type_street in type_proezd:
		type_street = "проезд"
	if type_street in type_pereulok:
		type_street = "переулок"
	return type_street


# возвращает статус объекта (0 на учете, 1 снят с учета)
def getRemoved(cadnum):
	url = 'http://rosreestr.ru/fir_lite_rest/api/gkn/fir_object/' + str(cadnum)
	r = requests.get(url, headers=headers, verify="CertBundle.pem")
	# разбираем respons ответ в формате json -  это словарь.
	# из словаря достаем пару ключа objectData, а из него removed (0 на учете, 1 снят с учета)
	a = r.json().get("objectData")
	removed = a.get("removed")
	return removed

# функция возвращает список кадастровых номеров земельных участков по адресу, исключая снятые с учета
# пример: getCadNumParcel("улица", "Пархоменко", "21")  ответ: ['42:30:505028:40']
def getCadNumParcel(type_street, street, house):
	url = 'https://rosreestr.ru/fir_lite_rest/api/gkn/address/' \
		  'fir_objects?macroRegionId=132000000000&regionId=132431000000&street=' + str(street) + '&house=' + str(house)
	r = requests.get(url, headers=headers, verify="CertBundle.pem")
	# print(r.json())
	cadNumParcel = []
	for a in r.json():
		print("a = ", a)
		cadnum = a.get("objectCn")
		_type_street = a.get("street")
		index = _type_street.find("|")
		_type_street= _type_street[index + 1:]
		if a.get("objectType") == "parcel" and\
			getRemoved(cadnum) == 0 and\
			normalizationTypeStreet(type_street) == normalizationTypeStreet(_type_street):
			cadNumParcel.append(cadnum)
	return cadNumParcel

def getCadNumBuilding(type_street, street, house):
	url = 'https://rosreestr.ru/fir_lite_rest/api/gkn/address/' \
		  'fir_objects?macroRegionId=132000000000&regionId=132431000000&street=' + str(street) + '&house=' + str(house)
	r = requests.get(url, headers=headers, verify="CertBundle.pem")
	# print(r.json())
	cadNumBuilding = []
	for a in r.json():
		# print("a = ",a)
		cadnum = a.get("objectCn")
		_type_street = a.get("street")
		index = _type_street.find("|")
		_type_street = _type_street[index + 1:]
		if a.get("objectType") == "building" and\
			getRemoved(cadnum) == 0 and\
			normalizationTypeStreet(type_street) == normalizationTypeStreet(_type_street):
			cadNumBuilding.append(cadnum)
	return cadNumBuilding

def getCadNumApartment(type_street, street, house, apartment):
	url = 'https://rosreestr.ru/fir_lite_rest/api/gkn/address/' \
		  'fir_objects?macroRegionId=132000000000&regionId=132431000000&street=' + str(street) + '&house=' + str(house) + '&apartment=' + str(apartment)
	r = requests.get(url, headers=headers, verify="CertBundle.pem")
	# print(r.json())
	cadNumBuilding = []
	cadnum1 = "None"
	for a in r.json():
		print("a = ", a)
		if a.get("objectCn"):
			cadnum1 = a.get("objectCn")
		else:
			cadnum1 = "None"
	return cadnum1

def getTypeObject(cadnum):
	url = 'http://rosreestr.ru/fir_lite_rest/api/gkn/fir_object/' + str(cadnum)
	r = requests.get(url, headers=headers, verify="CertBundle.pem")
	a = r.json().get("objectData")
	if a.get("objectName"):
		objectName = a.get("objectName")
	else:
		objectName = 'None'
	return(objectName)

# функция возвращает список кадастровых номеров земельных участков по адресу,
# перебирая адреса с дефисом и без в номере здания
def getFullCadNumParcel(type_street, street, house):
	houses = [house]
	cadNumParcels = []
	if "-" in house:
		houses.append(str(house.replace("-", '')))
	for house in houses:
		cadNumParcel1 = getCadNumParcel(type_street, street, house)
		cadNumParcels = cadNumParcels + cadNumParcel1
	return cadNumParcels

def getFullCadNumBuilding(type_street, street, house):
	houses = [house]
	cadNumBuilding = []
	if "-" in house:
		houses.append(str(house.replace("-", '')))
	for house in houses:
		cadNumBuilding1 = getCadNumBuilding(type_street, street, house)
		cadNumBuilding = cadNumBuilding + cadNumBuilding1
	return cadNumBuilding

if __name__ == "__main__":
	print(getFullCadNumParcel("улица", "Сибирская", "45"))

# Другие варианты url:

# https://rosreestr.ru/fir_lite_rest/api/gkn/address/fir_objects?macroRegionId=132000000000&regionId=132431000000&street=Франкфурта&house=8&apartment=1
# http://rosreestr.ru/api/online/fir_object/42:30:301069:1456