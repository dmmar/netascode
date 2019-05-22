# Nework as Code. Nac model.
![alt text](https://github.com/dmmar/nac/blob/master/images/The_NaC_model.png?raw=true)
![alt text](https://github.com/dmmar/nac/blob/master/images/The_Main_Components.png?raw=true)

# 1. Ansible configuration:
```
> napalm-ansible (in python env)
open Ansible/ansible.cfg
Change these lines (# NAPALM)
```
# 2. Ansible/Python_scripts:

generate-prod-diff.py and generate-test-diff.py
```
Generate ssh key for client workstation

line16 # GIT_MASTER_DIR = "/Volumes/DATA/NaC_git_master/master"

line27 # Repo.clone_from('git@github.com:dmmar/NetDevOps.git',

line30 # SRC_DIR_MASTER = os.path.abspath("/Volumes/DATA/NaC_git_master/master/CiscoDevNet/Ansible/inventories/production/host_vars/")

line31 # SRC_DIR_BRANCH = os.path.abspath("/Volumes/DATA/Network_as_Code/NetDevOps/CiscoDevNet/Ansible/inventories/production/host_vars/")
```
# 3. Ansible/inventories/production/group_vars/all.yaml:
```
line9 # config_dir: /Volumes/DATA/Network_as_Code/NetDevOps/CiscoDevNet/Ansible/inventories/production/CONFIGS
```
```
ansible_user: 'cisco'
ansible_ssh_pass: 'cisco'
ansible_connection: network_cli
ansible_network_os: ios
```

# 4. Ansible/inventories/test/group_vars/all.yaml:
```
line9 # config_dir: /Volumes/DATA/Network_as_Code/NetDevOps/CiscoDevNet/Ansible/inventories/test/CONFIGS
```
```
ansible_user: 'cisco'
ansible_ssh_pass: 'cisco'
ansible_connection: network_cli
ansible_network_os: ios
```

# 5. Ansible/inventories/production/hosts

# 6. Ansible/inventories/test/hosts


# 7. .gitlab-ci.yml

INSTALLING NAPALM FOR ANSIBLE

```
rm -f CiscoDevNet/Ansible/ansible.cfg
mv CiscoDevNet/GitLab_installation/local/ansible.cfg CiscoDevNet/Ansible/
echo "===================================================="
cd CiscoDevNet/Ansible
```

# 8. Docker-runner folder
```
Docker-runner/gitlab-napalm-config-dir.sh
```

# 9. Checking:
```
ansible -i inventories/test/hosts ALL -m ping
```
```
ansible -i inventories/production/hosts ALL -m ping
```