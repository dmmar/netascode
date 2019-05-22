#!/usr/bin/python

#########
# TEST  #
#########

import os
import hashlib
from git import Repo
from git import Git
import shutil

# PATH TO DIR WHERE GIT WILL COPY MASTER BRANCH TO COMPARE
# WHEN THE SCRIPT WILL RUN THAT DELETES 'MASTER' FOLDER AND DOWNLOAD A NEW

GIT_MASTER_DIR = "/home/dmitrii/Desktop/nac_master_branch/master"

if os.path.isdir(GIT_MASTER_DIR):
    shutil.rmtree(GIT_MASTER_DIR)

# USE SSH-KEY FOR DOWNLOAD A PRIVATE REPO

git_ssh_identity_file = os.path.expanduser('~/.ssh/id_rsa')
git_ssh_cmd = 'ssh -i %s' % git_ssh_identity_file

with Git().custom_environment(GIT_SSH_COMMAND=git_ssh_cmd):
     Repo.clone_from('git@github.com:dmmar/nac.git', GIT_MASTER_DIR, branch='master')

# PATH TO FOLDERS WHERE 'MD5' WILL CHECK CHECKSUM 'host_vars' FILES BETWEEN 'MASTER' and 'BRANCH'
SRC_DIR_MASTER = os.path.abspath("/home/dmitrii/Desktop/nac_master_branch/master/Ansible/inventories/test/host_vars/")
SRC_DIR_BRANCH = os.path.abspath("/home/dmitrii/PycharmProjects/nac/Ansible/inventories/test/host_vars")

for root, subdirs, files in os.walk(SRC_DIR_MASTER):
    checksums_master = []
    for file in files:
        with open(os.path.join(root, file), 'rb') as _file:
            checksums_master.append([file, hashlib.md5(_file.read()).hexdigest()])

for root, subdirs, files in os.walk(SRC_DIR_BRANCH):
    checksums_branch = []
    for file in files:
        with open(os.path.join(root, file), 'rb') as _file:
            checksums_branch.append([file, hashlib.md5(_file.read()).hexdigest()])

WHATEVER = [i for i, j in zip(checksums_master, checksums_branch) if i != j]

VALUES = ', '.join(str(v) for v in WHATEVER)

FIX_STR1 = VALUES.replace("[", "")
FIX_STR2 = FIX_STR1.replace("]", "")

LIST_SPLIT = FIX_STR2.split(', ')

NEW_LIST = [v for i, v in enumerate(LIST_SPLIT) if i % 2 == 0]

FIX_STR3 = ','.join(NEW_LIST)

FIX_STR4 = FIX_STR3.replace(".yaml", "")
FIX_STR5 = FIX_STR4.replace("'", "")

FINAL_STR = '--limit ' + FIX_STR5

print('Use this line for generate "FULL" config and make diff (...ONLY FOR DEVICES WHICH WERE CHANGED...)')
print("================================================================================================")
print('ansible-playbook -i inventories/test/hosts Modules/generate/generate-all-config-and-make-diff.yml', FINAL_STR)