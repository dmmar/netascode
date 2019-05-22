# Example
# -------
#
#   connectivity_check_v2.py

from pyats import aetest
import re
import logging

# get your logger for your script
logger = logging.getLogger(__name__)

class CommonSetup(aetest.CommonSetup):

# CommonSetup-SubSec1

    @aetest.subsection
    def check_topology(
            self,
            testbed,
            HQ_C1_name = 'HQ-C1',
            HQ_C2_name = 'HQ-C2',
            HQ_C3_name = 'HQ-C3',
            HQ_C4_name = 'HQ-C4',
            BR1_C1_name = 'BR1-C1',
            BR2_C1_name = 'BR2-C1'):

        HQ_C1 = testbed.devices[HQ_C1_name]
        HQ_C2 = testbed.devices[HQ_C2_name]
        HQ_C3 = testbed.devices[HQ_C3_name]
        HQ_C4 = testbed.devices[HQ_C4_name]
        BR1_C1 = testbed.devices[BR1_C1_name]
        BR2_C1 = testbed.devices[BR2_C1_name]

        # add them to testscript parameters
        self.parent.parameters.update(
            HQ_C1 = HQ_C1,
            HQ_C2 = HQ_C2,
            HQ_C3 = HQ_C3,
            HQ_C4 = HQ_C4,
            BR1_C1 = BR1_C1,
            BR2_C1 = BR2_C1)

# CommonSetup-SubSec

    @aetest.subsection
    def establish_connections(self, steps, HQ_C1, HQ_C2, HQ_C3, HQ_C4, BR1_C1, BR2_C1):
        with steps.start('Connecting to %s' % HQ_C1.name):
            HQ_C1.connect()

        with steps.start('Connecting to %s' % HQ_C2.name):
            HQ_C2.connect()

        with steps.start('Connecting to %s' % HQ_C3.name):
            HQ_C3.connect()

        with steps.start('Connecting to %s' % HQ_C4.name):
            HQ_C4.connect()

        with steps.start('Connecting to %s' % BR1_C1.name):
            BR1_C1.connect()

        with steps.start('Connecting to %s' % BR2_C1.name):
            BR2_C1.connect()


    @aetest.subsection
    def setup_ip_addresses(self, steps, HQ_C1, HQ_C2, HQ_C3, HQ_C4, BR1_C1, BR2_C1):
        with steps.start('Setup static IPv4 to %s' % HQ_C1.name):
            HQ_C1.execute('ip 10.255.100.10/27 10.255.100.1')

        with steps.start('Setup static IPv4 to %s' % HQ_C2.name):
            HQ_C2.execute('ip 10.255.100.40/27 10.255.100.33')

        with steps.start('Setup static IPv4 to %s' % HQ_C3.name):
            HQ_C3.execute('ip 10.255.100.70/27 10.255.100.65')

        with steps.start('Setup static IPv4 to %s' % HQ_C4.name):
            HQ_C4.execute('ip 10.255.100.100/27 10.255.100.97')

        with steps.start('Setup static IPv4 to %s' % BR1_C1.name):
            BR1_C1.execute('ip 10.1.100.10/27 10.1.100.1')

        with steps.start('Setup static IPv4 to %s' % BR2_C1.name):
            BR2_C1.execute('ip 10.2.100.10/27 10.2.100.1')

# TestCases

class TESTCASE_1_PING_FROM_HQ_CLIENTS_TO_ISP(aetest.Testcase):

    @aetest.test
    def T1_PING_FROM_HQ_C1_TO_ISP(self, HQ_C1):
        try:
            result = HQ_C1.execute('ping 8.8.8.8 -c 5')
        except Exception as e:
            self.failed('Something go wrong'.format(str(e)), goto = ['exit'])
        else:
            match = re.search('timeout', result) or re.search('not reachable|unreachable', result)
            print('################')
            print('Result is =>', result)
            print('Math is =>', match)
            print('################')
            if match:
                print('Math is => FIND', match)
                print('################')
                self.failed()
            else:
                print('Math is => NOT FIND')
                print('################')

    @aetest.test
    def T2_PING_FROM_HQ_C2_TO_ISP(self, HQ_C2):
        try:
            result = HQ_C2.execute('ping 8.8.8.8 -c 5')
        except Exception as e:
            self.failed('Something go wrong'.format(str(e)), goto = ['exit'])
        else:
            match = re.search('timeout', result) or re.search('not reachable|unreachable', result)
            print('################')
            print('Result is =>', result)
            print('Math is =>', match)
            print('################')
            if match:
                print('Math is => FIND', match)
                print('################')
                self.failed()
            else:
                print('Math is => NOT FIND')
                print('################')

    @aetest.test
    def T3_PING_FROM_HQ_C3_TO_ISP(self, HQ_C3):
        try:
            result = HQ_C3.execute('ping 8.8.8.8 -c 5')
        except Exception as e:
            self.failed('Something go wrong'.format(str(e)), goto=['exit'])
        else:
            match = re.search('timeout', result) or re.search('not reachable|unreachable', result)
            print('################')
            print('Result is =>', result)
            print('Math is =>', match)
            print('################')
            if match:
                print('Math is => FIND', match)
                print('################')
                self.failed()
            else:
                print('Math is => NOT FIND')
                print('################')

    @aetest.test
    def T4_PING_FROM_HQ_C4_TO_ISP(self, HQ_C4):
        try:
            result = HQ_C4.execute('ping 8.8.8.8 -c 5')
        except Exception as e:
            self.failed('Something go wrong'.format(str(e)), goto=['exit'])
        else:
            match = re.search('timeout', result) or re.search('not reachable|unreachable', result)
            print('################')
            print('Result is =>', result)
            print('Math is =>', match)
            print('################')
            if match:
                print('Math is => FIND', match)
                print('################')
                self.failed()
            else:
                print('Math is => NOT FIND')
                print('################')

class TESTCASE_2_PING_FROM_BR1_CLIENTS_TO_ISP(aetest.Testcase):

    @aetest.test
    def T1_PING_FROM_BR1_C1_TO_ISP(self, BR1_C1):
        try:
            result = BR1_C1.execute('ping 8.8.8.8 -c 5')
        except Exception as e:
            self.failed('Something go wrong'.format(str(e)), goto = ['exit'])
        else:
            match = re.search('timeout', result) or re.search('not reachable|unreachable', result)
            print('################')
            print('Result is =>', result)
            print('Math is =>', match)
            print('################')
            if match:
                print('Math is => FIND', match)
                print('################')
                self.failed()
            else:
                print('Math is => NOT FIND')
                print('################')

class TESTCASE_3_PING_FROM_BR2_CLIENTS_TO_ISP(aetest.Testcase):

    @aetest.test
    def T1_PING_FROM_BR2_C1_TO_ISP(self, BR2_C1):
        try:
            result = BR2_C1.execute('ping 8.8.8.8 -c 5')
        except Exception as e:
            self.failed('Something go wrong'.format(str(e)), goto = ['exit'])
        else:
            match = re.search('timeout', result) or re.search('not reachable|unreachable', result)
            print('################')
            print('Result is =>', result)
            print('Math is =>', match)
            print('################')
            if match:
                print('Math is => FIND', match)
                print('################')
                self.failed()
            else:
                print('Math is => NOT FIND')
                print('################')

class TESTCASE_4_PING_FROM_HQ_CLIENTS_TO_HQ_S1(aetest.Testcase):

    @aetest.test
    def T1_PING_FROM_HQ_C1_TO_HQ_S1(self, HQ_C1):
        try:
            result = HQ_C1.execute('ping 10.255.255.2 -c 5')
        except Exception as e:
            self.failed('Something go wrong'.format(str(e)), goto = ['exit'])
        else:
            match = re.search('timeout', result) or re.search('not reachable|unreachable', result)
            print('################')
            print('Result is =>', result)
            print('Math is =>', match)
            print('################')
            if match:
                print('Math is => FIND', match)
                print('################')
                self.failed()
            else:
                print('Math is => NOT FIND')
                print('################')

    @aetest.test
    def T2_PING_FROM_HQ_C2_TO_HQ_S1(self, HQ_C2):
        try:
            result = HQ_C2.execute('ping 10.255.255.2 -c 5')
        except Exception as e:
            self.failed('Something go wrong'.format(str(e)), goto = ['exit'])
        else:
            match = re.search('timeout', result) or re.search('not reachable|unreachable', result)
            print('################')
            print('Result is =>', result)
            print('Math is =>', match)
            print('################')
            if match:
                print('Math is => FIND', match)
                print('################')
                self.failed()
            else:
                print('Math is => NOT FIND')
                print('################')

    @aetest.test
    def T3_PING_FROM_HQ_C3_TO_HQ_S1(self, HQ_C3):
        try:
            result = HQ_C3.execute('ping 10.255.255.2 -c 5')
        except Exception as e:
            self.failed('Something go wrong'.format(str(e)), goto=['exit'])
        else:
            match = re.search('timeout', result) or re.search('not reachable|unreachable', result)
            print('################')
            print('Result is =>', result)
            print('Math is =>', match)
            print('################')
            if match:
                print('Math is => FIND', match)
                print('################')
                self.failed()
            else:
                print('Math is => NOT FIND')
                print('################')

    @aetest.test
    def T4_PING_FROM_HQ_C4_TO_HQ_S1(self, HQ_C4):
        try:
            result = HQ_C4.execute('ping 10.255.255.2 -c 5')
        except Exception as e:
            self.failed('Something go wrong'.format(str(e)), goto=['exit'])
        else:
            match = re.search('timeout', result) or re.search('not reachable|unreachable', result)
            print('################')
            print('Result is =>', result)
            print('Math is =>', match)
            print('################')
            if match:
                print('Math is => FIND', match)
                print('################')
                self.failed()
            else:
                print('Math is => NOT FIND')
                print('################')

class TESTCASE_5_PING_FROM_BR1_CLIENTS_TO_HQ_S1(aetest.Testcase):

    @aetest.test
    def T1_PING_FROM_BR1_C1_TO_HQ_S1(self, BR1_C1):
        try:
            result = BR1_C1.execute('ping 10.255.255.2 -c 5')
        except Exception as e:
            self.failed('Something go wrong'.format(str(e)), goto = ['exit'])
        else:
            match = re.search('timeout', result) or re.search('not reachable|unreachable', result)
            print('################')
            print('Result is =>', result)
            print('Math is =>', match)
            print('################')
            if match:
                print('Math is => FIND', match)
                print('################')
                self.failed()
            else:
                print('Math is => NOT FIND')
                print('################')

class TESTCASE_6_PING_FROM_BR2_CLIENTS_TO_HQ_S1(aetest.Testcase):

    @aetest.test
    def T1_PING_FROM_BR2_C1_TO_HQ_S1(self, BR2_C1):
        try:
            result = BR2_C1.execute('ping 10.255.255.2 -c 5')
        except Exception as e:
            self.failed('Something go wrong'.format(str(e)), goto = ['exit'])
        else:
            match = re.search('timeout', result) or re.search('not reachable|unreachable', result)
            print('################')
            print('Result is =>', result)
            print('Math is =>', match)
            print('################')
            if match:
                print('Math is => FIND', match)
                print('################')
                self.failed()
            else:
                print('Math is => NOT FIND')
                print('################')

class TESTCASE_7_TRACEROUTE_FROM_HQ_CLIENTS_TO_ISP(aetest.Testcase):

    @aetest.test
    def T1_TRACE_FROM_HQ_C1_TO_ISP(self, HQ_C1):
        try:
            result = HQ_C1.execute('trace 8.8.8.8')
        except Exception as e:
            self.failed('Something go wrong'.format(str(e)), goto = ['exit'])
        else:
            match = re.search('\*+[*]?$', result)
            print('################')
            print('Result is =>', result)
            print('Math is =>', match)
            print('################')
            if match:
                print('Math is => FIND', match)
                print('################')
                self.failed()
            else:
                print('Math is => NOT FIND')
                print('################')

    @aetest.test
    def T2_TRACE_FROM_HQ_C2_TO_ISP(self, HQ_C2):
        try:
            result = HQ_C2.execute('trace 8.8.8.8')
        except Exception as e:
            self.failed('Something go wrong'.format(str(e)), goto = ['exit'])
        else:
            match = re.search('\*+[*]?$', result)
            print('################')
            print('Result is =>', result)
            print('Math is =>', match)
            print('################')
            if match:
                print('Math is => FIND', match)
                print('################')
                self.failed()
            else:
                print('Math is => NOT FIND')
                print('################')

    @aetest.test
    def T3_TRACE_FROM_HQ_C3_TO_ISP(self, HQ_C3):
        try:
            result = HQ_C3.execute('trace 8.8.8.8')
        except Exception as e:
            self.failed('Something go wrong'.format(str(e)), goto = ['exit'])
        else:
            match = re.search('\*+[*]?$', result)
            print('################')
            print('Result is =>', result)
            print('Math is =>', match)
            print('################')
            if match:
                print('Math is => FIND', match)
                print('################')
                self.failed()
            else:
                print('Math is => NOT FIND')
                print('################')

    @aetest.test
    def T4_TRACE_FROM_HQ_C4_TO_ISP(self, HQ_C4):
        try:
            result = HQ_C4.execute('trace 8.8.8.8')
        except Exception as e:
            self.failed('Something go wrong'.format(str(e)), goto = ['exit'])
        else:
            match = re.search('\*+[*]?$', result)
            print('################')
            print('Result is =>', result)
            print('Math is =>', match)
            print('################')
            if match:
                print('Math is => FIND', match)
                print('################')
                self.failed()
            else:
                print('Math is => NOT FIND')
                print('################')

# CommonCleanup

class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect(self, steps, HQ_C1, HQ_C2, HQ_C3, HQ_C4, BR1_C1, BR2_C1):
        with steps.start('Disconnecting from %s' % HQ_C1.name):
            HQ_C1.disconnect()

        with steps.start('Disconnecting from %s' % HQ_C2.name):
            HQ_C2.disconnect()

        with steps.start('Disconnecting from %s' % HQ_C3.name):
            HQ_C3.disconnect()

        with steps.start('Disconnecting from %s' % HQ_C4.name):
            HQ_C4.disconnect()

        with steps.start('Disconnecting from %s' % BR1_C1.name):
            BR1_C1.disconnect()

        with steps.start('Disconnecting from %s' % BR2_C1.name):
            BR2_C1.disconnect()

if __name__ == '__main__':
    import argparse
    from pyats.topology import loader

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest = 'testbed',
                        type = loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))