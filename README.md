## Network as Code. NaC model.

### Overview

### Prerequisites

* PyCharm CE
* Python3.6
* Python virtualenv
* pip3
* git
* Docker and docker-compose
(for NetBox, GitLab CE, and docker-runner containers)
* GNS3

I personally tested on Ubuntu 18.04.2 LTS and PyCharm CE

For Ubuntu also needs:

* apt-get install python3-setuptools
* apt-get install python3-pip


### Installation

### Step 0

    # git clone https://github.com/dmmar/netascode.git
    
    # pip3 -r requirements.txt

### Step 1 (Ansible module napalm-ansible)

    Ansible/ansible.cfg

Configure ansible to use napalm
After napalm installation you need to configure proper path to library at ansible.cfg file. Example is below.

$ **napalm-ansible**

To ensure Ansible can use the NAPALM modules you will have
to add the following configuration to your Ansible configuration
file (ansible.cfg):

    [defaults]
    library = /Library/Python/2.7/site-packages/napalm_ansible/modules
    action_plugins = /Library/Python/2.7/site-packages/napalm_ansible/plugins/action

For more details on ansible's configuration file visit:
https://docs.ansible.com/ansible/latest/intro_configuration.html

### Step X (optional)

    To build docker containers such as NetBox, GitLab CE, and docker-runner:
        
    WARNING: DO NOT use these containers in real production environment 
    (NetBox has predefined values for DB passwords, secrets and etc.)
    
    **For correct installation - Read official documentation!**
    
    WARNING2: Installation_components/NetBox/docker-compose.yml has predefined values, 
    for example: gitlab.nac.local:192.168.1.100.
    
    For my project host 192.168.1.100 was a VM Debian with installed Docker and docker-compose.
   More information: https://www.netascode.com/?p=166

    To install docker-compose and disable firewall:

    # cd Installation_components
    # chmod +x docker_compose_setup.sh
    # ./docker_compose_setup.sh
    
    To install docker containers using docker-compose.yml file:
    
    # cd Installation_components/NetBox
    # docker-compose up -d
    # docker ps

### Step X (optional)

If you want to make an ansible final commmand to generate configs,

only for devices in 'host_vars' directory which you changed.

You need to fix these:

    /home/dmitrii/PycharmProjects/netascode/Ansible/Python_scripts/generate_diff
    
For files:
* generate-prod-diff.py
* generate-test-diff.py

Need to change to **your absolute path**

    GIT_MASTER_DIR = "/home/dmitrii/Desktop/netascode_master_branch/master"
    
    # PATH TO FOLDERS WHERE 'MD5' WILL CHECK CHECKSUM 'host_vars' FILES BETWEEN 'MASTER' and 'BRANCH'
    SRC_DIR_MASTER = os.path.abspath("/home/dmitrii/Desktop/netascode_master_branch/master/Ansible/inventories/production/host_vars/")
    SRC_DIR_BRANCH = os.path.abspath("/home/dmitrii/PycharmProjects/nac/Ansible/inventories/production/host_vars")


### References

* https://github.com/DevNetSandbox/sbx_multi_ios
* https://github.com/fooelisa/napalm_demo
* https://github.com/dbarrosop/ansible_demo
* https://github.com/kecorbin/pyats-network-checks
* https://github.com/kecorbin/pyats-ios-sample
* https://github.com/DreamLab/ansible-vyos
* https://github.com/tktkban/rfdemo
* https://github.com/permitanyany/robotframework
* https://github.com/networktocode/ntc-templates
* https://github.com/google/textfsm