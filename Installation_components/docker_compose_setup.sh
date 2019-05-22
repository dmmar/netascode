#!/usr/bin/env bash

echo ""
echo "Installation and checking docker-compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
docker-compose --version

echo ""
echo "Ensuring firewalld is stopped and disabled"
sudo systemctl stop firewalld
sudo systemctl disable firewalld
sudo systemctl restart docker
