import os
from genie.conf import Genie
# import the topology module
from ats.topology import loader

# import the genie libs
from genie.abstract import Lookup
from genie.libs import ops

# load testbed file which describes our devices
pyats_testbed = loader.load('testbed.yaml')

# pyats testbed != genie testbed
genie_testbed = Genie.init(pyats_testbed)
print(genie_testbed.devices)
all_interfaces = dict()

for name, device in genie_testbed.devices.items():
    print("Gathering Interface Information from {}".format(name))
    device.connect()
    abstract = Lookup.from_device(device)
    intf = abstract.ops.interface.interface.Interface(device)
    intf.learn()
    all_interfaces[name] = intf.info

for device, ints in all_interfaces.items():
    for name, props in ints.items():
        counters = props.get('counters')
        if counters:
            print('{}:{} CRC Errors: {}'.format(device,
                                                name,
                                                counters['in_crc_errors']))