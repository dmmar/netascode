# Example
# -------
#
#   ntp_check.py for Cisco IOS, Cisco ASA, VyOS, JunOS

from pyats import aetest
import re
import logging
from pyats.log.utils import banner


logger = logging.getLogger(__name__)

class CommonSetup(aetest.CommonSetup):

# CommonSetup-SubSec

    @aetest.subsection
    def topology(self, testbed, devices):

        for ios_name in devices:
            if ios_name not in testbed:
                self.failed('testbed needs to contain device {ios_name}'.format(ios_name=ios_name),
                            goto = ['exit'])

        device_list = devices

        for d in device_list:

            device = testbed.devices[d]

            logger.info(banner(
                "Connect to device '{d}'".format(d=device)))
            try:

                device.connect()

            except Exception as e:
                msg = "Failed to connect to {}"
                logger.info(msg.format(device))

class TESTCASE_1(aetest.Testcase):

    @ aetest.test
    def GET_NTP_INFO(self, testbed, devices, ntp_server):

        device_list = devices

        for d in device_list:

            device = testbed.devices[d]

            logger.info(banner(
                "Getting OS from '{d}'".format(d=device)))

            try:

                os_type = device.type

                asa_match = re.search('ASA', os_type)

                if asa_match:

                    command = device.execute('show run ntp')

                    ntp_match = re.search(ntp_server, command)

                    if ntp_match:
                        print('=' * 50)
                        print('NTP SERVER IS CORRECT on {}'.format(device))
                        print('=' * 50)
                    else:
                        print('=' * 50)
                        print('NTP SERVER IS NOT CORRECT on {}'.format(device))
                        print('=' * 50)
                        self.failed()

            except Exception as e:
                msg = "Failed to execute command to {}"
                logger.info(msg.format(device))

            try:

                os_type = device.type

                ios_match = re.search('IOS', os_type)

                if ios_match:

                    command = device.execute('show run | s ntp')

                    ntp_match = re.search(ntp_server, command)

                    if ntp_match:
                        print('=' * 50)
                        print('NTP SERVER IS CORRECT on {}'.format(device))
                        print('=' * 50)
                    else:
                        print('=' * 50)
                        print('NTP SERVER IS NOT CORRECT on {}'.format(device))
                        print('=' * 50)
                        self.failed()

            except Exception as e:
                msg = "Failed to execute command to {}"
                logger.info(msg.format(device))

            try:

                os_type = device.type

                vyos_match = re.search('VYOS', os_type)

                if vyos_match:

                    command = device.execute('show ntp')

                    ntp_match = re.search(ntp_server, command)

                    if ntp_match:
                        print('=' * 50)
                        print('NTP SERVER IS CORRECT on {}'.format(device))
                        print('=' * 50)
                    else:
                        print('=' * 50)
                        print('NTP SERVER IS NOT CORRECT on {}'.format(device))
                        print('=' * 50)
                        self.failed()

            except Exception as e:
                msg = "Failed to execute command to {}"
                logger.info(msg.format(device))

            try:

                os_type = device.type

                junos_match = re.search('JUNOS', os_type)

                if junos_match:

                    command = device.execute('show configuration system ntp')

                    ntp_match = re.search(ntp_server, command)

                    if ntp_match:
                        print('=' * 50)
                        print('NTP SERVER IS CORRECT on {}'.format(device))
                        print('=' * 50)
                    else:
                        print('=' * 50)
                        print('NTP SERVER IS NOT CORRECT on {}'.format(device))
                        print('=' * 50)
                        self.failed()

            except Exception as e:
                msg = "Failed to execute command to {}"
                logger.info(msg.format(device))


if __name__ == '__main__':
    import argparse
    from pyats.topology import loader

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest = 'testbed', type = loader.load, required=True)
    parser.add_argument('--devices', dest = 'devices', nargs='+', required=True)
    parser.add_argument('--ntp-server', dest='ntp_server', type=str, required=True)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))