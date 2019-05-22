# -*- coding: utf-8 -*-

from netmiko import ConnectHandler


class NetmikoOperator():

    def __init__(self):
        self.net_connect = {}
        self.device = ""

    def open_session(self,ip,username,password,device,hostname):
        # open session to target device
        if hostname in self.net_connect:
            pass
        else:
            # make SSH session to device
            handler = {
                'device_type': device,
                'ip': ip,
                'username': username,
                'password': password,
                }
            self.net_connect[hostname] = ConnectHandler(**handler)
            self.device = device
            print("[INFO] Successfully make SSH connection to {}".format(hostname))

    def close_session(self,hostname):
        # close existing session
        self.net_connect[hostname].disconnect()
        del self.net_connect[hostname]
        print("[INFO] Successfully close SSH connection to {}".format(hostname))

    def send_command(self,command,hostname):
        # send command to target device
        out = self.net_connect[hostname].send_command(command)
        print("[INFO] Successfully get output of command <{}> from {}".format(command,hostname))
        print("="*30)
        print(out)
        print("="*30)
        return out

    def send_commands_from_file(self,hostname,file_name=''):
        # send command to target device
        out = self.net_connect[hostname].send_config_from_file(config_file=file_name)
        print("="*30)
        print(out)
        print("="*30)
        print("[INFO] Successfully sent commands to {} from file {}".format(hostname, file_name))
        return out

    def save_config(self,hostname):
        # save config for target device
        out = self.net_connect[hostname].save_config()
        print("="*30)
        print(out)
        print("="*30)
        print("[INFO] Successfully save config for {}".format(hostname))
        return out
