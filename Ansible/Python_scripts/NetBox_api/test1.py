import pynetbox

nb = pynetbox.api(url='http://192.168.1.100:8080/', token='agmi4q0owhteubbp5wtttg43ka53fsw4o8bojuw5')

all_devices = nb.dcim.devices.all()

print(all_devices)

all_devices = nb.dcim.devices.get(1)

print(all_devices)

print(all_devices.serial)
