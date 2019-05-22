# Example
# -------
#
#   rollback.py for Cisco IOS, Cisco ASA, VyOS, JunOS

######################################
# ROLLBACK IS ONLY FOR ONE STEP BACK #
######################################

############################################################################
# 'Cisco ASA' and 'VyOS' will be REBOOTED after run commands for rollback  #
############################################################################

#   FOR CISCO ASA ON THE FLASH MUST EXIST 'rollback_config.txt'
#
#   BECAUSE FOR 'COMMIT-MERGE' CONFIGURATION FOR CISCO ASA USING 'PYTHON SCRIPT'

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
    def ROLLBACK(self, testbed, devices):

        device_list = devices

        for d in device_list:

            device = testbed.devices[d]

            logger.info(banner(
                "Getting OS from '{d}'".format(d=device)))

            try:

                os_type = device.type
                asa_match = re.search('ASA', os_type)

                if asa_match:

                    try:

                        command1 = device.execute('copy /noconfirm flash:/rollback_config.txt startup-config')
                        command2 = device.execute('reload noconfirm')

                        print(command1)
                        print(command2)

                    except Exception as e:
                        self.failed('Device {} \'Rollback\' is failed: '
                                    .format(device, str(e)),
                                    goto=['exit'])
                    else:
                        print('For {} ROLLBACK IS COMPLETED SUCCESSFULLY'.format(device))

            except Exception as e:
                msg = "Failed to find match from {}"
                logger.info(msg.format(device))

            try:

                os_type = device.type

                ios_match = re.search('IOS', os_type)

                if ios_match:

                    try:

                        command1 = device.execute('configure replace flash:rollback_config.txt force')
                        command2 = device.execute('wr')

                        print(command1)
                        print(command2)

                    except Exception as e:
                        self.failed('Device {} \'Rollback\' is failed: '
                                    .format(device, str(e)),
                                    goto=['exit'])
                    else:
                        print('For {} ROLLBACK IS COMPLETED SUCCESSFULLY'.format(device))

            except Exception as e:
                msg = "Failed to find match from {}"
                logger.info(msg.format(device))

            try:

                os_type = device.type

                vyos_match = re.search('VYOS', os_type)

                if vyos_match:

                    try:

                        command1 = device.execute('configure')
                        command2 = device.execute('rollback 1')
                        command3 = device.execute('y')

                        print(command1)
                        print(command2)
                        print(command3)

                    except Exception as e:
                        self.failed('Device {} \'Rollback\' is failed: '
                                    .format(device, str(e)),
                                    goto=['exit'])
                    else:
                        print('For {} ROLLBACK IS COMPLETED SUCCESSFULLY'.format(device))

            except Exception as e:
                msg = "Failed to find match from {}"
                logger.info(msg.format(device))

            try:

                os_type = device.type

                junos_match = re.search('JUNOS', os_type)

                if junos_match:

                    try:

                        command1 = device.execute('edit')
                        command2 = device.execute('rollback 1')
                        command3 = device.execute('commit')

                        print(command1)
                        print(command2)
                        print(command3)

                    except Exception as e:
                        self.failed('Device {} \'Rollback\' is failed: '
                                    .format(device, str(e)),
                                    goto=['exit'])
                    else:
                        print('For {} ROLLBACK IS COMPLETED SUCCESSFULLY'.format(device))

            except Exception as e:
                msg = "Failed to find match from {}"
                logger.info(msg.format(device))


if __name__ == '__main__':
    import argparse
    from pyats.topology import loader

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest = 'testbed', type = loader.load, required=True)
    parser.add_argument('--devices', dest = 'devices', nargs='+', required=True)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))