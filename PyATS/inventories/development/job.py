# Example: job.py
# -------------------

from pyats.easypy import run
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--ntp-server', dest='ntp_server', type=str, required=True)
parser.add_argument('--devices', dest = 'devices', nargs='+', required=True)
args = parser.parse_args()

ntp_server = args.ntp_server
devices = args.devices

def main():

    # run api launches a testscript as an individual task.

    run('ntp_check_v2_no_rollback.py', devices=devices, ntp_server=ntp_server)

#    run('ntp_check_v3.py', devices = devices, ntp_server = ntp_server)