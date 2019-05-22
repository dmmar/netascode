# Example: job1.py
# -------------------
#
#   a simple job file for the script above

from pyats.easypy import run

def main():

    # run api launches a testscript as an individual task.
    run('vlans_check.py')
