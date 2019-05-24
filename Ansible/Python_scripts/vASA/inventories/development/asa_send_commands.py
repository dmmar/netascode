import NetmikoOperator

# Import class 'NetmikoOperator' from module 'NetmikoOperator.py'
a = NetmikoOperator.NetmikoOperator()

ip = '192.168.4.108'
username = 'cisco'
password = 'cisco'
device = 'cisco_asa'
hostname = 'HQ-FW1'
file_name = '/home/dmitrii/PycharmProjects/netascode/Ansible/inventories/development/CONFIGS/HQ-FW1/FINAL_pre.conf'
command = 'copy /noconfirm run flash:/rollback_config.txt'

# files = []
# config_filename = hostname + ".txt"
# files.append(config_filename)
#
# # Get running-config from Cisco-ASA
# commands = ['show run']

a.open_session(ip,username,password,device,hostname)

# for command in commands:
#     this_cmd = a.send_command(command,hostname)
#     config_filename_f = open(config_filename, 'a')
#     config_filename_f.write(this_cmd)
#     config_filename_f.write('\n')
#     config_filename_f.close()

# To make a backup of previous configuration for rollback
a.send_command(command, hostname)

a.send_commands_from_file(hostname,file_name)

a.save_config(hostname)

a.close_session(hostname)







