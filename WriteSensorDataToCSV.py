'''
Read measurements from GoDirect Sensors in SAM

Locations:

al = Airlock
cq = Crew Quarters
eb = Engineering Bay
kn = Kitchen
ll = Lower Lung
tm = Test Module

Data files are written in the following format:

[YYYYMMDDHHSS]_[Location]_[Data Type]_[MiscInfo].csv
'''

import csv
import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
# warnings.simplefilter("ignore")


from time import strftime
from gdx import gdx

gdx = gdx.gdx()

location = input('Enter the location of the sensor (al | cq | eb | kn | ll): ')
datatype = input('Enter the type of data being monitored (co2 | db | o2 | ph | odo): ')
miscinfo = input('Enter miscellaneous location info if needed: ')
numofreadings = input('Readings are every 5 seconds. How many readings do you want? ')
numofreadings = int(numofreadings)

if datatype == 'o2':
    sensors = [1,2,3]
    device = 'GDX-O2 0R104011'
elif datatype == 'co2':
    sensors = [1,2,3]
    device = 'GDX-CO2 0Q400360'
elif datatype == 'db':
    sensors = [2,3]
    device = 'GDX-SND 0T3000S6'
elif datatype == 'ph':
    sensors = [1,2]
    device = 'GDX-EA 064004P2'
elif datatype == 'odo':
    sensors = [1,2,3,4,5]
    device = 'GDX-ODO 0N3003J8'
    

if miscinfo == '':
    datafilename = strftime('%Y%m%d%H%M')+'_'+location+'_'+datatype+'.csv'
else:
    datafilename = strftime('%Y%m%d%H%M')+'_'+location+'_'+datatype+'_'+miscinfo+'.csv'

gdx.open(connection='ble',device_to_open=device)   # Use connection='ble' for a Bluetooth connection

gdx.select_sensors(sensors)


with open(datafilename, 'w', newline='',encoding='utf-8') as my_data_file:
    csv_writer = csv.writer(my_data_file)

    gdx.start(period=5000)
    column_headers = gdx.enabled_sensor_info()
    column_headers=['timestamp']+column_headers
    csv_writer.writerow(column_headers)

    for i in range(0,numofreadings):
        measurements = gdx.read()
        measurements = [(strftime('%Y%m%d%H%M%S'))]+measurements
        if measurements == None:
            break

        csv_writer.writerow(measurements)
        print(measurements)

gdx.stop()
gdx.close()