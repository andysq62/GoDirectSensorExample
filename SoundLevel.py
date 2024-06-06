from gdx import gdx
gdx = gdx.gdx()


gdx.open(connection='usb', device_to_open='GDX-SND 0T3000S6')
gdx.select_sensors([2,3])
gdx.start() 
column_headers= gdx.enabled_sensor_info()   # returns a string with sensor description and units
print('\n')
print(column_headers)

for i in range(0,5):
    measurements = gdx.read()
    if measurements == None: 
        break 
    print(measurements)

gdx.stop()
gdx.close()