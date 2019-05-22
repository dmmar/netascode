#!/usr/bin/env bash

old_test='config_dir: /home/dmitrii/PycharmProjects/nac/Ansible/inventories/test/CONFIGS'
old_prod='config_dir: /home/dmitrii/PycharmProjects/nac/Ansible/inventories/production/CONFIGS'
new_test='config_dir: inventories/test/CONFIGS'
new_prod='config_dir: inventories/production/CONFIGS'
cd ..
# CHANGING PATH FOR DOCKER-RUNNER
sed -e "s|$old_test|$new_test|" Ansible/inventories/test/group_vars/all.yaml > Ansible/inventories/test/group_vars/all_new.yaml && mv Ansible/inventories/test/group_vars/all_new.yaml Ansible/inventories/test/group_vars/all.yaml
sed -e "s|$old_prod|$new_prod|" Ansible/inventories/production/group_vars/all.yaml > Ansible/inventories/production/group_vars/all_new.yaml && mv Ansible/inventories/production/group_vars/all_new.yaml Ansible/inventories/production/group_vars/all.yaml