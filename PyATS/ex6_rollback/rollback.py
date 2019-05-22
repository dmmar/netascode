# Example
# -------
#
#   rollback.py

from pyats import aetest
import logging
import textfsm
from pyats.log.utils import banner

# get your logger for your script
logger = logging.getLogger(__name__)

class CommonSetup(aetest.CommonSetup):

# CommonSetup-SubSec1

    @aetest.subsection
    def check_topology(
            self,
            testbed,
            ISP_name = 'ISP',
            BR1_ED1_name = 'VyOS-BR1-ED1',
            HQ_FW1_name = 'HQ-FW1',
            BR2_FW1_name = 'vSRX-BR2-FW1'):

        ISP = testbed.devices[ISP_name]
        BR1_ED1 = testbed.devices[BR1_ED1_name]
        HQ_FW1 = testbed.devices[HQ_FW1_name]
        BR2_FW1 = testbed.devices[BR2_FW1_name]


        # add them to testscript parameters
        self.parent.parameters.update(
            ISP = ISP,
            BR1_ED1 = BR1_ED1,
            HQ_FW1 = HQ_FW1,
            BR2_FW1 = BR2_FW1)

# CommonSetup-SubSec

    @aetest.subsection
    def establish_connections(self, steps, ISP, BR1_ED1, HQ_FW1, BR2_FW1):
        with steps.start('Connecting to %s' % ISP.name):
            ISP.connect()
        with steps.start('Connecting to %s' % BR1_ED1.name):
            BR1_ED1.connect()
        with steps.start('Connecting to %s' % HQ_FW1.name):
           HQ_FW1.connect()
        with steps.start('Connecting to %s' % BR2_FW1.name):
            BR2_FW1.connect()

# TestCases

class TESTCASE_1(aetest.Testcase):

    @aetest.test
    def ROLLBACK_ISP(self, ISP):
        try:

            command1 = ISP.execute('configure replace flash:rollback_config.txt force')
            command2 = ISP.execute('wr')

            print(command1)
            print(command2)

        except Exception as e:
            self.failed('Device {} \'Rollback\' is failed: '
                        .format(ISP, str(e)),
                        goto=['exit'])
        else:
            print('ROLLBACK IS COMPLETED SUCCESSFULLY')

    @aetest.test
    def ROLLBACK_HQ_FW1(self, HQ_FW1):
        try:

            command1 = HQ_FW1.execute('copy /noconfirm flash:/rollback_config.txt startup-config')
            command2 = HQ_FW1.execute('reload noconfirm')

            print(command1)
            print(command2)

        except Exception as e:
            self.failed('Device {} \'Rollback\' is failed: '
                        .format(HQ_FW1, str(e)),
                        goto=['exit'])
        else:
            print('ROLLBACK IS COMPLETED SUCCESSFULLY')

    @aetest.test
    def ROLLBACK_BR1_ED1(self, BR1_ED1):
        try:

            command1 = BR1_ED1.execute('configure')
            command2 = BR1_ED1.execute('rollback 1')
            command3 = BR1_ED1.execute('y')

            print(command1)
            print(command2)
            print(command3)

        except Exception as e:
            self.failed('Device {} \'Rollback\' is failed: '
                        .format(BR1_ED1, str(e)),
                        goto=['exit'])
        else:
            print('ROLLBACK IS COMPLETED SUCCESSFULLY')

    @aetest.test
    def ROLLBACK_BR2_FW1(self, BR2_FW1):
        try:

            command1 = BR2_FW1.execute('edit')
            command2 = BR2_FW1.execute('rollback 1')
            command3 = BR2_FW1.execute('commit')

            print(command1)
            print(command2)
            print(command3)

        except Exception as e:
            self.failed('{} \'Rollback\' is failed: '
                        .format(BR2_FW1, str(e)),
                        goto=['exit'])
        else:
            print('ROLLBACK IS COMPLETED SUCCESSFULLY')

# CommonCleanup

class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect(self, steps, ISP, BR2_FW1):
        with steps.start('Disconnecting from %s' % ISP.name):
            ISP.disconnect()
        with steps.start('Disconnecting from %s' % BR2_FW1.name):
            BR2_FW1.disconnect()

if __name__ == '__main__':
    import argparse
    from pyats.topology import loader

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest = 'testbed',
                        type = loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))