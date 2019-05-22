# Example
# -------
#
#   Demonstration of pyATS Robot Framework Keywords

*** Settings ***
# Importing test libraries, resource files and variable files.
Library        OperatingSystem
Library        vlans_check.py
Library        pyats.robot.pyATSRobot

*** Variables ***
# Defining variables that can be used elsewhere in the test data.
# Can also be driven as dash argument at runtime

${testbed}       testbed.yaml

*** Test Cases ***
# Creating test cases from available keywords.

Initialize
    # select the testbed to use
    use testbed "${testbed}"

CommonSetup
    # calling pyats common_setup
    run testcase "vlans_check.CommonSetup"

Testcase pass
    # calling pyats tes${device1} tcase
    run testcase "vlans_check.TESTCASE_1"

CommonCleanup
    run testcase "vlans_check.CommonCleanup"
