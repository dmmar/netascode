# Example
# -------
#
#   Demonstration of pyATS Robot Framework

*** Settings ***

Library        OperatingSystem
Library        pyats.robot.pyATSRobot
Library        vlans_check.py
Library        connectivity_check_v2.py

*** Variables ***

${testbed_1}       testbed_1.yaml
${testbed_2}       testbed_2.yaml

*** Test Cases ***

T1_Initialize
    [Documentation]    Loading 'testbed_1'
    use testbed "${testbed_1}"

T1_CommonSetup
    [Documentation]    CommonSetup for vlans_check.py
    run testcase "vlans_check.CommonSetup"

T1_Testcase pass
    run testcase "vlans_check.TESTCASE_1"

T1_CommonCleanup
    [Documentation]    CommonCleanup for vlans_check.py
    run testcase "vlans_check.CommonCleanup"

T2_Initialize
    [Documentation]    Loading 'testbed_2'
    use testbed "${testbed_2}"

T2_CommonSetup
    [Documentation]    CommonSetup for connectivity_check_v2.py
    run testcase "connectivity_check_v2.CommonSetup"

T2_Testcase1 pass
    run testcase "connectivity_check_v2.TESTCASE_1_PING_FROM_HQ_CLIENTS_TO_ISP"

T2_Testcase2 pass
    run testcase "connectivity_check_v2.TESTCASE_2_PING_FROM_BR1_CLIENTS_TO_ISP"

T2_Testcase3 pass
    run testcase "connectivity_check_v2.TESTCASE_3_PING_FROM_BR2_CLIENTS_TO_ISP"

T2_Testcase4 pass
    run testcase "connectivity_check_v2.TESTCASE_4_PING_FROM_HQ_CLIENTS_TO_HQ_S1"

T2_Testcase5 pass
    run testcase "connectivity_check_v2.TESTCASE_5_PING_FROM_BR1_CLIENTS_TO_HQ_S1"

T2_Testcase6 pass
    run testcase "connectivity_check_v2.TESTCASE_6_PING_FROM_BR2_CLIENTS_TO_HQ_S1"

T2_Testcase7 pass
    run testcase "connectivity_check_v2.TESTCASE_7_TRACEROUTE_FROM_HQ_CLIENTS_TO_ISP"

T2_CommonCleanup
    [Documentation]    CommonCleanup for connectivity_check_v2.py
    run testcase "connectivity_check_v2.CommonCleanup"
