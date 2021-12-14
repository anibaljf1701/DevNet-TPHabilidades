import requests
import json
#import urllib.parse
from prettytable import PrettyTable
from requests.api import request

main_url_api = 'https://api.meraki.com/api/v1/'
headers = {
    "X-Cisco-Meraki-Api-Key": "REDACTED"
}

###Paso 1: Obtener los id de las organizaciones###
#Armo la url
url_org = main_url_api + 'organizations'

#Genero la consulta para conseguir los IDs de las organizaciones
response_org = requests.request('GET', url_org, headers = headers, verify= True)
response_org_json = response_org.json()

#Armo la tabla de organizaciones con la libreria prettytable
table_org = response_org_json
table = PrettyTable(["ID","NAME"])
for table_org in table_org:
    table.add_row([table_org["id"],table_org["name"]])
#Imprimo la tabla
print('TABLA DE ORGANIZACIONES: ')
print(table)
print("\n")


###Paso 2: Obtener las redes de una organización a partir de la elección de un id del servicio anterior###
#Obtengo el ID de una organizacion
id_org = str(response_org_json[0]['id'])

#Armo la url
url_net = url_org + '/' + id_org + '/networks'

#Genero la consulta para conseguir las redes de la organizacion obtenida
response_net = requests.request('GET', url_net, headers = headers, verify= True)
response_net_json = response_net.json()

#Armo la tabla de redes de una organizacion con la libreria prettytable
table_net = response_net_json
table = PrettyTable(["ID","NAME"])
for table_net in table_net:
    table.add_row([table_net["id"],table_net["name"]])
#Imprimo la tabla
print('TABLA DE REDES DE UNA ORGANIZACION: ')
print(table)
print("\n")


###Paso 3: Obtener los dispositivos de la red pasándole como parámetro el networkid###
#Obtengo el networkID
id_net = str(response_net_json[0]['id'])

#Armo la url
url_devices = main_url_api + 'networks/' + id_net + '/devices'

#Genero la consulta para conseguir los dispositivos de una red obtenida
response_devices = requests.request('GET', url_devices, headers = headers, verify= True)
response_devices_json = response_devices.json()

#Armo la tabla de dispositivos de una red con la libreria prettytable
table_devices = response_devices_json
table = PrettyTable(["NAME" ,"MODEL", "SERIAL"])
for table_devices in table_devices:
    table.add_row([table_devices["name"],table_devices["model"], table_devices["serial"]])
#Imprimo la tabla
print('TABLA DE LOS DISPOSITIVOS DE UNA RED: ')
print(table)
print("\n")



###Paso 4: Obtener datos de la  red con el networkid###
#Armo la url
url_net_info = main_url_api + 'networks/' + id_net

#Genero la consulta para obtener los datos de una red
response_net_info = requests.request('GET', url_net_info, headers = headers, verify = True)
response_net_info_json = response_net_info.json()

print('INFORMACION DE LA RED: ')
print("NAME: " + response_net_info_json["name"])
print("ID: " + response_net_info_json["id"])
print("ORGANIZATION ID: " + response_net_info_json["organizationId"])
print("TIME ZONE: " + response_net_info_json["timeZone"])
print("\n")



###Paso 5: Obtener infomación de un dispositivo con el serial id###
#Obtengo el serial
serial_device = str(response_devices_json[0]['serial'])

#Armo la url
url_devices_info =  main_url_api + 'networks/' + id_net + '/devices/' + serial_device

#Genero la consulta para obtener los datos de un dispositivo
response_device_info = requests.request('GET', url_devices_info, headers = headers, verify = True)
response_device_info_json = response_device_info.json()

#print(response_device_info_json)
print('INFORMACION DE UN DISPOSITIVO DE LA RED: ')
print("NAME: " + response_device_info_json["name"])
print("SERIAL: " + response_device_info_json["serial"])
print("MAC: " + response_device_info_json["mac"])
print("MODEL: " + response_device_info_json["model"])
print("FIRMWARE: " + response_device_info_json["firmware"])
print("\n")



###Paso 6: Obtener información del SSID para el network ID###
#Armo la URL
url_ssid_info =  main_url_api + 'networks/' + id_net + '/wireless/ssids'

#Genero la consulta del SSID para un determinado network ID
response_ssid_info = requests.request('GET', url_ssid_info, headers = headers, verify = True)
response_ssid_info_json = response_ssid_info.json()

#Armo la tabla de la inforamcion de una red con la libreria prettytable
table_ssid_info = response_ssid_info_json
table = PrettyTable(["NUMBER","NAME","STATUS"])
for table_ssid_info in table_ssid_info:
    table.add_row([table_ssid_info["number"],table_ssid_info["name"],table_ssid_info["enabled"]])
#Imprimo la tabla
print('INFORMACION DE LOS SSID PARA UN NETWORK_ID: ')
print(table)