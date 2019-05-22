# Example
# -------
#
#   vlans_check.py

from pyats import aetest
import logging
import textfsm
from pyats.log.utils import banner


# TextFSM template for cisco_ios_show_vlan
template = open('cisco_ios_show_vlan.template')

# Compare these vlans [lists] with output from device (# show vlan br)
vlan10 = ['10', 'Sales', 'active']
vlan20 = ['20', 'Managers', 'active']
vlan30 = ['30', 'Developers', 'active']
vlan40 = ['40', 'Accounting', 'active']


# get your logger for your script
logger = logging.getLogger(__name__)

class CommonSetup(aetest.CommonSetup):

# CommonSetup-SubSec1

    @aetest.subsection
    def check_topology(
            self,
            testbed,
            HQ_DIS1_name = 'HQ-DIS1',
            HQ_DIS2_name = 'HQ-DIS2',
            HQ_AC1_name = 'HQ-AC1',
            HQ_AC2_name = 'HQ-AC2',
            HQ_AC3_name = 'HQ-AC3',
            HQ_AC4_name = 'HQ-AC4'):

        HQ_DIS1 = testbed.devices[HQ_DIS1_name]
        HQ_DIS2 = testbed.devices[HQ_DIS2_name]
        HQ_AC1 = testbed.devices[HQ_AC1_name]
        HQ_AC2 = testbed.devices[HQ_AC2_name]
        HQ_AC3 = testbed.devices[HQ_AC3_name]
        HQ_AC4 = testbed.devices[HQ_AC4_name]


        # add them to testscript parameters
        self.parent.parameters.update(
            HQ_DIS1 = HQ_DIS1,
            HQ_DIS2 = HQ_DIS2,
            HQ_AC1 = HQ_AC1,
            HQ_AC2 = HQ_AC2,
            HQ_AC3 = HQ_AC3,
            HQ_AC4 = HQ_AC4)

# CommonSetup-SubSec

    @aetest.subsection
    def establish_connections(self, steps, HQ_DIS1, HQ_DIS2, HQ_AC1, HQ_AC2, HQ_AC3, HQ_AC4):
        with steps.start('Connecting to %s' % HQ_DIS1.name):
            HQ_DIS1.connect()
        with steps.start('Connecting to %s' % HQ_DIS2.name):
            HQ_DIS2.connect()
        with steps.start('Connecting to %s' % HQ_AC1.name):
            HQ_AC1.connect()
        with steps.start('Connecting to %s' % HQ_AC2.name):
            HQ_AC2.connect()
        with steps.start('Connecting to %s' % HQ_AC3.name):
            HQ_AC3.connect()
        with steps.start('Connecting to %s' % HQ_AC4.name):
            HQ_AC4.connect()

# TestCases

class TESTCASE_1(aetest.Testcase):

    @aetest.test
    def HQ_DIS1_SHOW_VLAN_BRIEF_CHECK(self, HQ_DIS1):
        try:
            # store execution result for later usage
            result = HQ_DIS1.execute('show vlan brief')

            results_template = textfsm.TextFSM(template)
            parsed_results = results_template.ParseText(result)

            # Will delete information about interfaces from the list
            vlan10_output = parsed_results[1]
            vlan10_output.pop()
            vlan20_output = parsed_results[2]
            vlan20_output.pop()
            vlan30_output = parsed_results[3]
            vlan30_output.pop()
            vlan40_output = parsed_results[4]
            vlan40_output.pop()

            if vlan10_output == vlan10:
                print('VLAN-10 - [EXISTS and ACTIVE]')
            else:
                logger.info(banner('VLAN-10 - [DOES NOT EXIST]'))
                self.failed()

            if vlan20_output == vlan20:
                print('VLAN-20 - [EXISTS and ACTIVE]')
            else:
                logger.info(banner('VLAN-20 - [DOES NOT EXIST]'))
                self.failed()

            if vlan30_output == vlan30:
                print('VLAN-30 - [EXISTS and ACTIVE]')
            else:
                logger.info(banner('VLAN-30 - [DOES NOT EXIST]'))
                self.failed()

            if vlan40_output == vlan40:
                print('VLAN-40 - [EXISTS and ACTIVE]')
            else:
                logger.info(banner('VLAN-40 - [DOES NOT EXIST]'))
                self.failed()

        except Exception as e:
            self.failed('Device {} \'show vlan brief\' failed: '
                        '{}'.format(HQ_AC1, str(e)),
                        goto=['exit'])
        else:
            print('ALL VLANS EXISTS')

    @aetest.test
    def HQ_DIS2_SHOW_VLAN_BRIEF_CHECK(self, HQ_DIS2):
        try:
            # store execution result for later usage
            result = HQ_DIS2.execute('show vlan brief')

            results_template = textfsm.TextFSM(template)
            parsed_results = results_template.ParseText(result)

            # Will delete information about interfaces from the list
            vlan10_output = parsed_results[1]
            vlan10_output.pop()
            vlan20_output = parsed_results[2]
            vlan20_output.pop()
            vlan30_output = parsed_results[3]
            vlan30_output.pop()
            vlan40_output = parsed_results[4]
            vlan40_output.pop()

            if vlan10_output == vlan10:
                print('VLAN-10 - [EXISTS and ACTIVE]')
            else:
                logger.info(banner('VLAN-10 - [DOES NOT EXIST]'))
                self.failed()

            if vlan20_output == vlan20:
                print('VLAN-20 - [EXISTS and ACTIVE]')
            else:
                logger.info(banner('VLAN-20 - [DOES NOT EXIST]'))
                self.failed()

            if vlan30_output == vlan30:
                print('VLAN-30 - [EXISTS and ACTIVE]')
            else:
                logger.info(banner('VLAN-30 - [DOES NOT EXIST]'))
                self.failed()

            if vlan40_output == vlan40:
                print('VLAN-40 - [EXISTS and ACTIVE]')
            else:
                logger.info(banner('VLAN-40 - [DOES NOT EXIST]'))
                self.failed()

        except Exception as e:
            self.failed('Device {} \'show vlan brief\' failed: '
                        '{}'.format(HQ_AC1, str(e)),
                        goto=['exit'])
        else:
            print('ALL VLANS EXISTS')

    @aetest.test
    def HQ_AC1_SHOW_VLAN_BRIEF_CHECK(self, HQ_AC1):
        try:
            # store execution result for later usage
            result = HQ_AC1.execute('show vlan brief')

            results_template = textfsm.TextFSM(template)
            parsed_results = results_template.ParseText(result)

            # Will delete information about interfaces from the list
            vlan10_output = parsed_results[1]
            vlan10_output.pop()
            # vlan20_output = parsed_results[2]
            # vlan20_output.pop()
            # vlan30_output = parsed_results[3]
            # vlan30_output.pop()
            # vlan40_output = parsed_results[4]
            # vlan40_output.pop()

            if vlan10_output == vlan10:
                print('VLAN-10 - [EXISTS and ACTIVE]')
            else:
                logger.info(banner('VLAN-10 - [DOES NOT EXIST]'))
                self.failed()

            # if vlan20_output == vlan20:
            #     print('VLAN-20 - [EXISTS and ACTIVE]')
            # else:
            #     logger.info(banner('VLAN-20 - [DOES NOT EXIST]'))
            #     self.failed()
            #
            # if vlan30_output == vlan30:
            #     print('VLAN-30 - [EXISTS and ACTIVE]')
            # else:
            #     logger.info(banner('VLAN-30 - [DOES NOT EXIST]'))
            #     self.failed()
            #
            # if vlan40_output == vlan40:
            #     print('VLAN-40 - [EXISTS and ACTIVE]')
            # else:
            #     logger.info(banner('VLAN-40 - [DOES NOT EXIST]'))
            #     self.failed()

        except Exception as e:
            self.failed('Device {} \'show vlan brief\' failed: '
                            '{}'.format(HQ_AC1, str(e)),
                        goto = ['exit'])
        else:
            print('ALL VLANS EXISTS')

    @aetest.test
    def HQ_AC2_SHOW_VLAN_BRIEF_CHECK(self, HQ_AC2):
        try:
            # store execution result for later usage
            result = HQ_AC2.execute('show vlan brief')

            results_template = textfsm.TextFSM(template)
            parsed_results = results_template.ParseText(result)

            # Will delete information about interfaces from the list
            # vlan10_output = parsed_results[1]
            # vlan10_output.pop()
            vlan20_output = parsed_results[1]
            vlan20_output.pop()
            # vlan30_output = parsed_results[3]
            # vlan30_output.pop()
            # vlan40_output = parsed_results[4]
            # vlan40_output.pop()

            # if vlan10_output == vlan10:
            #     print('VLAN-10 - [EXISTS and ACTIVE]')
            # else:
            #     logger.info(banner('VLAN-10 - [DOES NOT EXIST]'))
            #     self.failed()

            if vlan20_output == vlan20:
                print('VLAN-20 - [EXISTS and ACTIVE]')
            else:
                logger.info(banner('VLAN-20 - [DOES NOT EXIST]'))
                self.failed()

            # if vlan30_output == vlan30:
            #     print('VLAN-30 - [EXISTS and ACTIVE]')
            # else:
            #     logger.info(banner('VLAN-30 - [DOES NOT EXIST]'))
            #     self.failed()
            #
            # if vlan40_output == vlan40:
            #     print('VLAN-40 - [EXISTS and ACTIVE]')
            # else:
            #     logger.info(banner('VLAN-40 - [DOES NOT EXIST]'))
            #     self.failed()

        except Exception as e:
            self.failed('Device {} \'show vlan brief\' failed: '
                        '{}'.format(HQ_AC1, str(e)),
                        goto=['exit'])
        else:
            print('ALL VLANS EXISTS')

    @aetest.test
    def HQ_AC3_SHOW_VLAN_BRIEF_CHECK(self, HQ_AC3):
        try:
            # store execution result for later usage
            result = HQ_AC3.execute('show vlan brief')

            results_template = textfsm.TextFSM(template)
            parsed_results = results_template.ParseText(result)

            # Will delete information about interfaces from the list
            # vlan10_output = parsed_results[1]
            # vlan10_output.pop()
            # vlan20_output = parsed_results[2]
            # vlan20_output.pop()
            vlan30_output = parsed_results[1]
            vlan30_output.pop()
            # vlan40_output = parsed_results[4]
            # vlan40_output.pop()

            # if vlan10_output == vlan10:
            #     print('VLAN-10 - [EXISTS and ACTIVE]')
            # else:
            #     logger.info(banner('VLAN-10 - [DOES NOT EXIST]'))
            #     self.failed()
            #
            # if vlan20_output == vlan20:
            #     print('VLAN-20 - [EXISTS and ACTIVE]')
            # else:
            #     logger.info(banner('VLAN-20 - [DOES NOT EXIST]'))
            #     self.failed()

            if vlan30_output == vlan30:
                print('VLAN-30 - [EXISTS and ACTIVE]')
            else:
                logger.info(banner('VLAN-30 - [DOES NOT EXIST]'))
                self.failed()

            # if vlan40_output == vlan40:
            #     print('VLAN-40 - [EXISTS and ACTIVE]')
            # else:
            #     logger.info(banner('VLAN-40 - [DOES NOT EXIST]'))
            #     self.failed()

        except Exception as e:
            self.failed('Device {} \'show vlan brief\' failed: '
                        '{}'.format(HQ_AC1, str(e)),
                        goto=['exit'])
        else:
            print('ALL VLANS EXISTS')

    @aetest.test
    def HQ_AC4_SHOW_VLAN_BRIEF_CHECK(self, HQ_AC4):
        try:
            # store execution result for later usage
            result = HQ_AC4.execute('show vlan brief')

            results_template = textfsm.TextFSM(template)
            parsed_results = results_template.ParseText(result)

            # Will delete information about interfaces from the list
            # vlan10_output = parsed_results[1]
            # vlan10_output.pop()
            # vlan20_output = parsed_results[2]
            # vlan20_output.pop()
            # vlan30_output = parsed_results[3]
            # vlan30_output.pop()
            vlan40_output = parsed_results[1]
            vlan40_output.pop()

            # if vlan10_output == vlan10:
            #     print('VLAN-10 - [EXISTS and ACTIVE]')
            # else:
            #     logger.info(banner('VLAN-10 - [DOES NOT EXIST]'))
            #     self.failed()
            #
            # if vlan20_output == vlan20:
            #     print('VLAN-20 - [EXISTS and ACTIVE]')
            # else:
            #     logger.info(banner('VLAN-20 - [DOES NOT EXIST]'))
            #     self.failed()
            #
            # if vlan30_output == vlan30:
            #     print('VLAN-30 - [EXISTS and ACTIVE]')
            # else:
            #     logger.info(banner('VLAN-30 - [DOES NOT EXIST]'))
            #     self.failed()

            if vlan40_output == vlan40:
                print('VLAN-40 - [EXISTS and ACTIVE]')
            else:
                logger.info(banner('VLAN-40 - [DOES NOT EXIST]'))
                self.failed()

        except Exception as e:
            self.failed('Device {} \'show vlan brief\' failed: '
                        '{}'.format(HQ_AC1, str(e)),
                        goto=['exit'])
        else:
            print('ALL VLANS EXISTS')

# CommonCleanup

class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect(self, steps, HQ_DIS1, HQ_DIS2, HQ_AC1, HQ_AC2, HQ_AC3, HQ_AC4):
        with steps.start('Disconnecting from %s' % HQ_DIS1.name):
            HQ_DIS1.disconnect()
        with steps.start('Disconnecting from %s' % HQ_DIS2.name):
            HQ_DIS2.disconnect()
        with steps.start('Disconnecting from %s' % HQ_AC1.name):
            HQ_AC1.disconnect()
        with steps.start('Disconnecting from %s' % HQ_AC2.name):
            HQ_AC2.disconnect()
        with steps.start('Disconnecting from %s' % HQ_AC3.name):
            HQ_AC3.disconnect()
        with steps.start('Disconnecting from %s' % HQ_AC4.name):
            HQ_AC4.disconnect()

if __name__ == '__main__':
    import argparse
    from pyats.topology import loader

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest = 'testbed',
                        type = loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))