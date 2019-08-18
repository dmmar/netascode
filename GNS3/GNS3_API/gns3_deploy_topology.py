#!/usr/bin/env python
from netmiko import Netmiko
from prettytable import PrettyTable
import os
import pexpect
import requests
import random
import time
import subprocess
import yaml
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
    return gns3_appliances_dict


def gns3_show_projects(gns3_server):

    show_projects = requests.get(gns3_server + '/v2/projects')

    if show_projects:
        show_projects_dict = show_projects.json()
        projects_count = 0
        t_projects = PrettyTable(['Number', 'Name', 'Project ID', 'Project status'])
        for dictionary in show_projects_dict:
            projects_count += 1
            project_name = dictionary['name']
            project_id = dictionary['project_id']
            project_status = dictionary['status']
            t_projects.add_row([projects_count, project_name, project_id, project_status])
        return t_projects
    else:
        print('Can not show GNS3 projects because something went wrong.')


def gns3_show_available_nodes(gns3_server, project_id):

    r_get_nodes = requests.get(gns3_server + '/v2/projects/' + str(project_id) + '/nodes')
    r_get_nodes_dict = r_get_nodes.json()
    count_nodes = 0
    table_available_nodes = PrettyTable(['Number', 'Name', 'Node ID', 'Status', 'Console Port'])
    print()
    print('Available nodes are:')
    print('#' * 100)
    for dictionary in r_get_nodes_dict:
        avaiable_node_name = dictionary['name']
        avaiable_node_id = dictionary['node_id']
        avaiable_node_status = dictionary['status']
        avaiable_node_console = dictionary['console']
        count_nodes += 1
        table_available_nodes.add_row([count_nodes, avaiable_node_name,
                                       avaiable_node_id, avaiable_node_status, avaiable_node_console])
    print(table_available_nodes)


def gns3_show_links(gns3_server, project_id):

    r_get_nodes = requests.get(gns3_server + '/v2/projects/' + str(project_id) + '/nodes')
    r_get_nodes_dict = r_get_nodes.json()

    r_get_links = requests.get(gns3_server + '/v2/projects/' + str(project_id) + '/links')
    r_get_links_dict = r_get_links.json()

    number_links = 0

    print('Existing links are:')

    for dictionary_link in r_get_links_dict:
        node_link_pair = dictionary_link['nodes']
        link_id = dictionary_link['link_id']
        link_type = dictionary_link['link_type']
        number_links += 1
        print('#' * 100)
        # Shows Link-Pair
        for index, item in enumerate(node_link_pair):
            for dictionary_node in r_get_nodes_dict:
                node_id = dictionary_node['node_id']
                node_port_number = item
                node_id_link = node_port_number['node_id']
                if node_id == node_id_link:
                    node_name = dictionary_node['name']
                    for key, value in node_port_number.items():
                        if key == 'adapter_number':
                            print(number_links, '|', node_name, '|', key, value, '|', 'Link-ID:', link_id, '|',
                                  'Link-type:', link_type)


def gns3_create_new_project(gns3_server, gns3_code_topology_data):

    project_name = gns3_code_topology_data['project_name']
    payload_create_project = '{"name": "' + str(project_name) + '"}'
    create_project = requests.post(gns3_server + '/v2/projects', data=payload_create_project)

    if create_project:
        create_project_dict = create_project.json()
        new_project_id = create_project_dict['project_id']
        print('#' * 100)
        print('A new GNS3 project', '[' + project_name + ']', 'is created.', 'Project ID:', new_project_id)
        print('#' * 100)
        return new_project_id
    else:
        existed_projects = gns3_show_projects(gns3_server)
        create_project_dict = create_project.json()
        print(existed_projects)
        print(create_project_dict['message'])

        show_projects = requests.get(gns3_server + '/v2/projects')
        existed_projects_dict = show_projects.json()

        for dictionary_projects in existed_projects_dict:
            existed_project_name = dictionary_projects['name']
            if project_name == existed_project_name:
                existed_project_id = dictionary_projects['project_id']
                print(existed_project_name, '|', existed_project_id)
                ask = input('Do you want to continue? [y/n] :')
                if ask == 'y':
                    return existed_project_id
                elif ask == 'n':
                    exit()
                else:
                    exit()


def gns3_code_topology_open(gns3_topology_file):
    with open(gns3_topology_file, "r") as read_file:
        data = yaml.safe_load(read_file)
        return data


def gns3_start_all_nodes(gns3_server, project_id):

    print("""
    ╔═╗┌┬┐┌─┐┌─┐  ╦╦╦   ╔═╗┌┬┐┌─┐┬─┐┌┬┐  ┌─┐┬  ┬    ┌┐┌┌─┐┌┬┐┌─┐┌─┐ 
    ╚═╗ │ ├┤ ├─┘  ║║║   ╚═╗ │ ├─┤├┬┘ │   ├─┤│  │    ││││ │ ││├┤ └─┐ 
    ╚═╝ ┴ └─┘┴    ╩╩╩.  ╚═╝ ┴ ┴ ┴┴└─ ┴   ┴ ┴┴─┘┴─┘  ┘└┘└─┘─┴┘└─┘└─┘.
    """)

    r_get_nodes = requests.get(gns3_server + '/v2/projects/' + str(project_id) + '/nodes')
    r_get_nodes_dict = r_get_nodes.json()

    for dictionary_node in r_get_nodes_dict:
        if dictionary_node['status'] == 'stopped':
            # For Built-in VPCS, starting time 5 sec.
            if dictionary_node['node_type'] == 'vpcs':
                print(dictionary_node['name'], 'is starting.', 'node-id:', dictionary_node['node_id'])
                print('Starting time is 5 sec.')
                node_id = dictionary_node['node_id']
                url_start_node = gns3_server + '/v2/projects/' + str(project_id) + '/nodes/' + node_id + '/start'
                requests.post(url=url_start_node)
                print(time.ctime())
                time.sleep(5)
                print(dictionary_node['name'], 'is loaded.', time.ctime())
                print('#' * 100)
            # For Juniper vSRX, starting time 10 min.
            elif dictionary_node['port_name_format'] == 'ge-0/0/{0}':
                print(dictionary_node['name'], 'is starting.', 'node-id:', dictionary_node['node_id'])
                print('Starting time is 10 min.')
                node_id = dictionary_node['node_id']
                url_start_node = gns3_server + '/v2/projects/' + str(project_id) + '/nodes/' + node_id + '/start'
                requests.post(url=url_start_node)
                print(time.ctime())
                time.sleep(600)
                print(dictionary_node['name'], 'is loaded.', time.ctime())
                print('#' * 100)
            # For other GNS3 appliances, starting time 1 min.
            else:
                print(dictionary_node['name'], 'is starting.', 'node-id:', dictionary_node['node_id'])
                print('Starting time is 1 min.')
                node_id = dictionary_node['node_id']
                url_start_node = gns3_server + '/v2/projects/' + str(project_id) + '/nodes/' + node_id + '/start'
                requests.post(url=url_start_node)
                print(time.ctime())
                time.sleep(60)
                print(dictionary_node['name'], 'is loaded.', time.ctime())
                print('#' * 100)
        else:
            print(dictionary_node['name'], 'is working,', 'telnet port:',
                  dictionary_node['console'], ', node-id:', dictionary_node['node_id'])
    time.sleep(60)
    print('=' * 100)


def gns3_create_nodes(gns3_server, project_id, gns3_code_topology_data):

    print("""
    ╔═╗┌┬┐┌─┐┌─┐  ╦   ╔═╗┬─┐┌─┐┌─┐┌┬┐┌─┐  ┌┐┌┌─┐┌┬┐┌─┐┌─┐
    ╚═╗ │ ├┤ ├─┘  ║   ║  ├┬┘├┤ ├─┤ │ ├┤   ││││ │ ││├┤ └─┐
    ╚═╝ ┴ └─┘┴    ╩.  ╚═╝┴└─└─┘┴ ┴ ┴ └─┘  ┘└┘└─┘─┴┘└─┘└─┘.
    """)

    gns3_appliances = gns3_get_appliances_names_and_id(gns3_server)

    list_images = []
    list_node_names = []

    for node in gns3_code_topology_data['gns3_nodes']:
        appliance = node['appliance']
        name = node['name']
        r_get_nodes = requests.get(gns3_server + '/v2/projects/' + str(project_id) + '/nodes')
        r_get_nodes_dict = r_get_nodes.json()
        # Checking existence of nodes in the project from the topology file.
        for dictionary_node in r_get_nodes_dict:
            if dictionary_node['name'] == name:
                console_port = dictionary_node['console']
                status = dictionary_node['status']
                print(name, 'is already created.', 'Console port:', console_port, 'Status:', status)
                break
        else:  # the code in the else block runs only if the loop completes without encountering a break statement.
            list_images.append(appliance)
            list_node_names.append(name)
    if not list_node_names:
        print()
        print('All nodes were already created in GNS3 project.', 'Project ID:', project_id)
        print('#' * 100)
        return
    else:
        # Creating new nodes from the topology file.
        for node_image, node_name in zip(list_images, list_node_names):
            print()
            print('Pair:', '[' + node_image + ']', '[' + node_name + ']')

            payload_coordinates = '{"x": 0, "y": 0}'
            payload_create_node = '{"name": "' + node_name + '"}'

            for key, value in gns3_appliances.items():
                if node_image == key:
                    # Built in GNS3
                    if node_image == 'Cloud':
                        cloud_payload = '{"name": "' + node_name + \
                                        '", "node_type": "cloud", "compute_id": "local"}'
                        cloud_r = requests.post(gns3_server + '/v2/projects/' + project_id + '/nodes',
                                                data=cloud_payload)
                        if cloud_r:
                            cloud_r_dict = cloud_r.json()
                            cloud_new_id = cloud_r_dict['node_id']
                            print()
                            print(node_name, 'is created.', cloud_new_id)
                            print()
                            continue
                        else:
                            print(cloud_r)
                            print('that is not working, please try again.')
                            return
                    elif node_image == 'VPCS':
                        vpcs_payload = '{"name": "' + node_name + \
                                       '", "node_type": "vpcs", "compute_id": "local"}'
                        vpcs_r = requests.post(gns3_server + '/v2/projects/' + project_id + '/nodes', data=vpcs_payload)
                        if vpcs_r:
                            vpcs_r_dict = vpcs_r.json()
                            vpcs_new_id = vpcs_r_dict['node_id']
                            print()
                            print(node_name, 'is created.', vpcs_new_id)
                            print()
                            continue
                        else:
                            print(vpcs_r)
                            print('that is not working, please try again.')
                            return
                    elif node_image == 'NAT':
                        nat_payload = '{"name": "' + node_name + \
                                      '", "node_type": "nat", "compute_id": "local"}'
                        nat_r = requests.post(gns3_server + '/v2/projects/' + project_id + '/nodes', data=nat_payload)
                        if nat_r:
                            nat_r_dict = nat_r.json()
                            nat_new_id = nat_r_dict['node_id']
                            print()
                            print(node_name, 'is created.', nat_new_id)
                            print()
                            continue
                        else:
                            print(nat_r)
                            print('that is not working, please try again.')
                            return
                    elif node_image == 'Frame Relay switch':
                        fr_sw_payload = '{"name": "' + node_name + \
                                        '", "node_type": "frame_relay_switch", "compute_id": "local"}'
                        fr_sw_r = requests.post(gns3_server + '/v2/projects/' + project_id + '/nodes',
                                                data=fr_sw_payload)
                        if fr_sw_r:
                            fr_sw_r_dict = fr_sw_r.json()
                            fr_sw_new_id = fr_sw_r_dict['node_id']
                            print()
                            print(node_name, 'is created.', fr_sw_new_id)
                            print()
                            continue
                        else:
                            print(fr_sw_r)
                            print('that is not working, please try again.')
                            return
                    elif node_image == 'Ethernet hub':
                        eth_hub_payload = '{"name": "' + node_name + \
                                          '", "node_type": "ethernet_hub", "compute_id": "local"}'
                        eth_hub_r = requests.post(gns3_server + '/v2/projects/' + project_id + '/nodes',
                                                  data=eth_hub_payload)
                        if eth_hub_r:
                            eth_hub_r_dict = eth_hub_r.json()
                            eth_hub_new_id = eth_hub_r_dict['node_id']
                            print()
                            print(node_name, 'is created.', eth_hub_new_id)
                            print()
                            continue
                        else:
                            print(eth_hub_r)
                            print('that is not working, please try again.')
                            return
                    elif node_image == 'Ethernet switch':
                        eth_sw_payload = '{"name": "' + node_name + \
                                         '", "node_type": "ethernet_switch", "compute_id": "local"}'
                        eth_sw_r = requests.post(gns3_server + '/v2/projects/' + project_id + '/nodes',
                                                 data=eth_sw_payload)
                        if eth_sw_r:
                            eth_sw_r_dict = eth_sw_r.json()
                            eth_sw_new_id = eth_sw_r_dict['node_id']
                            print()
                            print(node_name, 'is created.', eth_sw_new_id)
                            print()
                            continue
                        else:
                            print(eth_sw_r)
                            print('that is not working, please try again.')
                            return
                    # Added manually
                    else:
                        appliance_id = value
                        r_create_node = requests.post(gns3_server + '/v2/projects/' + project_id + '/appliances/'
                                                      + appliance_id, data=payload_coordinates)
                        if r_create_node:
                            r_create_node_dict = r_create_node.json()
                            new_node_id = r_create_node_dict['node_id']
                            requests.put(gns3_server + '/v2/projects/' + project_id + '/nodes/' + new_node_id,
                                         data=payload_create_node)
                            print()
                            print(node_name, 'is created.', new_node_id)
                            print('#' * 100)
                        else:
                            print(r_create_node)
                            print('that is not working, please try again.')
                            exit()
        print('=' * 100)


def gns3_create_many_links(gns3_server, project_id, gns3_code_topology_data):

    print("""
    ╔═╗┌┬┐┌─┐┌─┐  ╦╦   ╔═╗┬─┐┌─┐┌─┐┌┬┐┌─┐  ╦  ┬┌┐┌┬┌─  ┌─┐┌─┐┬┬─┐┌─┐
    ╚═╗ │ ├┤ ├─┘  ║║   ║  ├┬┘├┤ ├─┤ │ ├┤   ║  ││││├┴┐  ├─┘├─┤│├┬┘└─┐
    ╚═╝ ┴ └─┘┴    ╩╩.  ╚═╝┴└─└─┘┴ ┴ ┴ └─┘  ╩═╝┴┘└┘┴ ┴  ┴  ┴ ┴┴┴└─└─┘.
    """)

    node1_list_devices = []
    node1_list_links = []

    node2_list_devices = []
    node2_list_links = []

    for link_pair in gns3_code_topology_data['gns3_links']:
        # Link-pair:
        node1_name = link_pair['node1_name']
        node1_interface = link_pair['node1_interface']
        node2_name = link_pair['node2_name']
        node2_interface = link_pair['node2_interface']

        node1_list_devices.append(node1_name)
        node1_list_links.append(node1_interface)
        node2_list_devices.append(node2_name)
        node2_list_links.append(node2_interface)

    for node1, node2, node1_link, node2_link in zip(node1_list_devices,
                                                    node2_list_devices,
                                                    node1_list_links,
                                                    node2_list_links):
        print('#' * 100)
        print('Pair:', node1, node2, node1_link, node2_link)
        print()
        r_get_nodes = requests.get(gns3_server + '/v2/projects/' + str(project_id) + '/nodes')
        r_get_nodes_dict = r_get_nodes.json()

        name_node1 = node1
        name_node2 = node2

        for dictionary_node in r_get_nodes_dict:

            node_name_local = dictionary_node['name']

            if node1 == node_name_local:
                print(node1, 'that device is existed in GNS3 project.')
                node1 = dictionary_node['node_id']
            if node2 == node_name_local:
                print(node2, 'that device is existed in GNS3 project.')
                node2 = dictionary_node['node_id']

        adapter_number_1 = node1_link
        adapter_number_2 = node2_link

        print()
        print(name_node1, 'is used a link number:', adapter_number_1)
        print(name_node2, 'is used a link number:', adapter_number_2)

        node_id_1 = '"' + node1 + '"'
        node_id_2 = '"' + node2 + '"'

        payload_create_link = '{"nodes": [{"adapter_number": ' + str(adapter_number_1) + ', "node_id": ' + str(node_id_1) + \
                              ', "port_number": 0}, {"adapter_number": ' + str(adapter_number_2) + ', "node_id": ' + \
                              str(node_id_2) + ', "port_number": 0}]}'

        r_create_link_pair = requests.post(gns3_server + '/v2/projects/' + project_id + '/links',
                                           data=payload_create_link)

        if r_create_link_pair:
            r_create_link_pair_dict = r_create_link_pair.json()
            print()
            print('New Link-ID:', r_create_link_pair_dict['link_id'])
        else:
            print()
            print(r_create_link_pair)
            print('A link pair is already created in the GNS3 project. Project ID:', project_id)
            continue
    print('=' * 100)


def gns3_send_start_config_telnet(gns3_server, project_id, gns3_code_topology_data, global_delay_factor):

    print("""
    ╔═╗┌┬┐┌─┐┌─┐  ╦╦  ╦  ┌─┐┌─┐┌┐┌┌┬┐  ┌─┐┌┬┐┌─┐┬─┐┌┬┐┬ ┬┌─┐  ┌─┐┌─┐┌┐┌┌─┐┬┌─┐
    ╚═╗ │ ├┤ ├─┘  ║╚╗╔╝  └─┐├┤ │││ ││  └─┐ │ ├─┤├┬┘ │ │ │├─┘  │  │ ││││├┤ ││ ┬
    ╚═╝ ┴ └─┘┴    ╩ ╚╝.  └─┘└─┘┘└┘─┴┘  └─┘ ┴ ┴ ┴┴└─ ┴ └─┘┴    └─┘└─┘┘└┘└  ┴└─┘.
    """)

    gns3_host_ip = gns3_code_topology_data['gns3_host_ip']
    START_CFGS_PATH = gns3_code_topology_data['START_CFGS_PATH']

    list_start_config_nodes = []

    for node in gns3_code_topology_data['gns3_startup_config_telnet']:
        name = node['name']
        list_start_config_nodes.append(name)

    for node_name in list_start_config_nodes:
        print()
        print('Applying startup config to', node_name + ' from',
              '[' + gns3_code_topology_data['START_CFGS_PATH'] + node_name + ']')
        print()

        r_get_nodes = requests.get(gns3_server + '/v2/projects/' + str(project_id) + '/nodes')
        r_get_nodes_dict = r_get_nodes.json()

        for dictionary_node in r_get_nodes_dict:
            if dictionary_node['name'] == node_name:
                # For VPCS
                if dictionary_node['node_type'] == 'vpcs':
                    device_type = 'generic_termserver_telnet'

                    config_path = os.path.abspath(START_CFGS_PATH + node_name)
                    telnet_port = dictionary_node['console']

                    device = {
                        "host": gns3_host_ip,
                        "device_type": device_type,
                        "port": telnet_port,
                        "global_delay_factor": global_delay_factor
                    }

                    net_connect = Netmiko(**device)
                    net_connect.send_config_from_file(config_file=config_path, exit_config_mode=False)
                    net_connect.disconnect()
                    continue
                # For VyOS.
                elif dictionary_node['port_name_format'] == 'eth{0}':
                    device_type = 'generic_termserver_telnet'

                    config_path = os.path.abspath(START_CFGS_PATH + node_name)
                    telnet_port = dictionary_node['console']

                    device = {
                        "host": gns3_host_ip,
                        "device_type": device_type,
                        "port": telnet_port,
                        "global_delay_factor": global_delay_factor
                    }

                    vyos = pexpect.spawn('telnet ' + gns3_host_ip + ' ' + str(telnet_port))
                    vyos.expect('')
                    vyos.sendline('\n')
                    vyos.expect('login: ')
                    vyos.sendline('vyos\n')
                    vyos.expect('Password:')
                    vyos.sendline('vyos')

                    net_connect = Netmiko(**device)
                    net_connect.send_config_from_file(config_file=config_path, exit_config_mode=False)
                    net_connect.disconnect()
                    continue
                # For JunOS.
                elif dictionary_node['port_name_format'] == 'ge-0/0/{0}':
                    device_type = 'juniper_junos_telnet'

                    config_path = os.path.abspath(START_CFGS_PATH + node_name)
                    telnet_port = dictionary_node['console']

                    device = {
                        "host": gns3_host_ip,
                        "device_type": device_type,
                        "port": telnet_port,
                        "global_delay_factor": global_delay_factor
                    }

                    juniper = pexpect.spawn('telnet ' + gns3_host_ip + ' ' + str(telnet_port))
                    juniper.expect('')
                    juniper.sendline('\n')
                    juniper.expect('login: ')
                    juniper.sendline('root\n')
                    juniper.expect('')
                    juniper.sendline('\n')
                    juniper.expect('root@% ', timeout=120)
                    juniper.sendline('cli')

                    with open(config_path) as f:
                        lines = f.read().splitlines()

                    net_connect = Netmiko(**device)
                    net_connect.config_mode()

                    for line in lines:
                        net_connect.send_command_timing(line)
                        time.sleep(1)
                    net_connect.disconnect()
                    continue
                # For Cisco IOS and Cisco ASA.
                else:
                    device_type = 'cisco_ios_telnet'

                    config_path = os.path.abspath(START_CFGS_PATH + node_name)
                    telnet_port = dictionary_node['console']

                    device = {
                        "host": gns3_host_ip,
                        "device_type": device_type,
                        "port": telnet_port,
                        "global_delay_factor": global_delay_factor
                    }

                    net_connect = Netmiko(**device)
                    net_connect.enable()
                    net_connect.send_config_from_file(config_file=config_path)
                    net_connect.disconnect()
                    continue
        print('Success -', node_name)
    print('=' * 100)


def gns3_create_mgmt_links(gns3_server, project_id, gns3_code_topology_data):

    print("""
    ╔═╗┌┬┐┌─┐┌─┐  ╦  ╦  ┌─┐┬─┐┌─┐┌─┐┌┬┐┌─┐  ┌┬┐┌─┐┌┬┐┌┬┐  ┬  ┬┌┐┌┬┌─┌─┐
    ╚═╗ │ ├┤ ├─┘  ╚╗╔╝  │  ├┬┘├┤ ├─┤ │ ├┤   ││││ ┬│││ │   │  ││││├┴┐└─┐
    ╚═╝ ┴ └─┘┴     ╚╝.  └─┘┴└─└─┘┴ ┴ ┴ └─┘  ┴ ┴└─┘┴ ┴ ┴   ┴─┘┴┘└┘┴ ┴└─┘.
    """)

    mgmt_sw = gns3_code_topology_data['MGMT-SW']
    if mgmt_sw is None:
        print('Skipped [create_mgmt_links] because MGMT-SW: null')
        print('#' * 100)
        return
    else:
        mgmt_sw_name = mgmt_sw
        list_mgmt_nodes = []

        for node in gns3_code_topology_data['gns3_mgmt_links']:
            name = node['name']
            list_mgmt_nodes.append(name)

        for node2 in list_mgmt_nodes:
            print()
            print('Pair:', mgmt_sw_name + ' - ' + node2)

            mgmt_sw_ints_used = []
            node2_ints_used = []

            mgmt_sw_ints_existed = []
            node2_ints_existed = []

            r_get_node_id = requests.get(gns3_server + '/v2/projects/' + str(project_id) + '/nodes')
            r_get_node_id_dict = r_get_node_id.json()

            r_get_links = requests.get(gns3_server + '/v2/projects/' + str(project_id) + '/links')
            r_get_links_dict = r_get_links.json()

            for dictionary2 in r_get_links_dict:
                loop = dictionary2['nodes']
                for dictionary_node in r_get_node_id_dict:
                    node_name_local = dictionary_node['name']
                    if mgmt_sw == node_name_local:
                        print(mgmt_sw, 'that device is existed in GNS3 project.')
                        mgmt_sw = dictionary_node['node_id']
                    if node2 == node_name_local:
                        print(node2, 'that device is existed in GNS3 project.')
                        node2 = dictionary_node['node_id']

                for index, item in enumerate(loop):
                        a = item
                        node_id = a['node_id']
                        if mgmt_sw == node_id:
                            for key, value in a.items():
                                if key == 'port_number':
                                    mgmt_sw_ints_used.append(value)
                        if node2 == node_id:
                            for key, value in a.items():
                                if key == 'adapter_number':
                                    node2_ints_used.append(value)

            for dictionary_node_id in r_get_node_id_dict:
                if mgmt_sw == dictionary_node_id['node_id']:
                    loop1 = dictionary_node_id['ports']
                    for index, item in enumerate(loop1):
                        a = item
                        for key, value in a.items():
                            if key == 'port_number':
                                mgmt_sw_ints_existed.append(value)

                if node2 == dictionary_node_id['node_id']:
                    loop2 = dictionary_node_id['ports']
                    for index, item in enumerate(loop2):
                        a = item
                        for key, value in a.items():
                            if key == 'adapter_number':
                                node2_ints_existed.append(value)

            diff1 = set(mgmt_sw_ints_existed) - set(mgmt_sw_ints_used)

            mgmt_sw_ints_free = list(diff1)

            def func_random_link_mgmt_sw():
                while mgmt_sw_ints_free:
                    random_link_mgmt_sw = random.choice(mgmt_sw_ints_free)
                    print()
                    print(random_link_mgmt_sw, 'random interface for', mgmt_sw_name)
                    return random_link_mgmt_sw

            port_number_1 = func_random_link_mgmt_sw()
            adapter_number_2 = '0'

            mgmt_sw_id = '"' + mgmt_sw + '"'
            node2_id = '"' + node2 + '"'

            payload = '{"nodes": [{"adapter_number": 0, "node_id": ' + str(mgmt_sw_id) + \
                      ', "port_number": ' + str(port_number_1) + '}, {"adapter_number": ' + \
                      str(adapter_number_2) + ', "node_id": ' + str(node2_id) + ', "port_number": 0}]}'

            r_create_mgmt_link = requests.post(gns3_server + '/v2/projects/' + project_id + '/links',
                                               data=payload)

            if r_create_mgmt_link:
                r_create_mgmt_link_dict = r_create_mgmt_link.json()
                print()
                print('#' * 50)
                print('New Link-ID:', r_create_mgmt_link_dict['link_id'])
                print('#' * 50)
            else:
                print(r_create_mgmt_link)
                print('A link pair is already created in the GNS3 project. Project ID:', project_id)
                print('=' * 100)
                continue
        print('=' * 100)


def gns3_ping_devices(gns3_code_topology_data):

    print("""
    ╔═╗┌┬┐┌─┐┌─┐  ╦  ╦╦   ╔═╗╦╔╗╔╔═╗  ┌┬┐┌─┐┬  ┬┬┌─┐┌─┐┌─┐
    ╚═╗ │ ├┤ ├─┘  ╚╗╔╝║   ╠═╝║║║║║ ╦   ││├┤ └┐┌┘││  ├┤ └─┐
    ╚═╝ ┴ └─┘┴     ╚╝ ╩.  ╩  ╩╝╚╝╚═╝  ─┴┘└─┘ └┘ ┴└─┘└─┘└─┘.
    """)

    # Ping network devices through a mgmt interface.
    with open(os.devnull, "wb") as limbo:
        for ip_mgmt in gns3_code_topology_data['gns3_nodes']:
            if 'ip_mgmt' in ip_mgmt:
                node_name = ip_mgmt['name']
                ip = ip_mgmt['ip_mgmt']
                result = subprocess.Popen(["ping", "-c", "5", "-n", "-W", "5", ip],
                                          stdout=limbo, stderr=limbo).wait()
                if result:
                    print(node_name, ip, "inactive")
                else:
                    print(node_name, ip, "active")
            else:
                node_name = ip_mgmt['name']
                print(node_name, 'does not have an IP MGMT address.')


def main():
    print("""
#######################
#     AUTO BUILD      #
#       STATIC        #
#        GNS3         #
#      TOPOLOGY       #
#######################
    """)
    # Takes a file from a cli argument and loads that GNS3 topology file.
    gns3_topology_file = args.gns3_topology_file
    gns3_code_topology_data = gns3_code_topology_open(gns3_topology_file)
    # Assigns gns3_server variable from GNS3 topology file.
    gns3_server = gns3_code_topology_data['gns3_server']
    # global_delay_factor for [gns3_send_start_config_telnet]
    # I used a global delay parameter because
    # my GNS3 server is located far away from me (380>= latency).
    global_delay_factor = gns3_code_topology_data['global_delay_factor']
    print('#' * 100)
    print('Deploying GNS3 topology from:', gns3_topology_file)
    print('Current GNS3 server is', gns3_server)
    start_time = time.ctime()
    print('Starting time:', start_time)
    print('#' * 100)
    # Assigns 'project_id' from a new created GNS3 project.
    project_id = gns3_create_new_project(gns3_server, gns3_code_topology_data)
    # Creates nodes from [gns3_nodes] in the topology file.
    gns3_create_nodes(gns3_server, project_id, gns3_code_topology_data)
    # Creates link pairs from [gns3_links] in the topology file.
    gns3_create_many_links(gns3_server, project_id, gns3_code_topology_data)
    # Starts all nodes. VPCS starting time 5 sec, JunOS vSRX starting time 10 min,
    # other such as Cisco IOSv, IOSvL2, etc. starting time 1 min.
    gns3_start_all_nodes(gns3_server, project_id)
    # Shows available nodes in the project.
    gns3_show_available_nodes(gns3_server, project_id)
    # Shows connected links in the project.
    gns3_show_links(gns3_server, project_id)
    # Sends startup config for nodes from [gns3_startup_config_telnet] in the topology file.
    gns3_send_start_config_telnet(gns3_server, project_id, gns3_code_topology_data, global_delay_factor)
    # Creates mgmt-link-pairs for nodes from [gns3_mgmt_links] in the topology file.
    gns3_create_mgmt_links(gns3_server, project_id, gns3_code_topology_data)
    # Pings nodes via mgmt interface.
    gns3_ping_devices(gns3_code_topology_data)
    print('#' * 100)
    print('Starting time:', start_time)
    print('Ending time:', time.ctime())
    print('#' * 100)
    print(gns3_show_projects(gns3_server))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='store', dest='gns3_topology_file', required=True,
                        help='GNS3 topology file as code, for example: gns3_dev_topology.yaml')
    args = parser.parse_args()
    main()
