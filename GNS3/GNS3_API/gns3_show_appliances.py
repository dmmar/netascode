#!/usr/bin/env python
import requests
from prettytable import PrettyTable
import argparse


def gns3_get_appliances_names_and_id(gns3_server):
    gns3_appliances_dict = {}
    show_appliances = requests.get(gns3_server + '/v2/appliances')
    if show_appliances:
        show_appliances_dict = show_appliances.json()
        for appliance in show_appliances_dict:
            gns3_get_appliance_name = appliance['name']
            gns3_get_appliance_id = appliance['appliance_id']
            gns3_show_appliances = gns3_get_appliance_name, gns3_get_appliance_id
            gns3_appliance_name = gns3_show_appliances[0]
            gns3_appliance_id = gns3_show_appliances[1]
            gns3_appliances_dict.update({gns3_appliance_name: gns3_appliance_id})
    else:
        print(show_appliances)
        print('that is not working.')
        exit()
    return gns3_appliances_dict


def main():
    gns3_appliances = gns3_get_appliances_names_and_id(gns3_server)
    t_available_appliances = PrettyTable(['Appliance Name', 'ID'])
    for key, value in gns3_appliances.items():
        t_available_appliances.add_row([key, value])
    print('#' * 100)
    print('Current GNS3 server is', gns3_server)
    print('Available appliances are:')
    print('#' * 100)
    print(t_available_appliances)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', action='store', dest='gns3_server', required=True,
                        help='GNS3 server, for example: http://172.16.1.1:3080')
    args = parser.parse_args()
    gns3_server = args.gns3_server
    main()
