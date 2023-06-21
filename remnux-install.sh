#!/bin/bash

# ubuntu 20.04

# Get the version number of the current distribution
version=$(lsb_release -sr)

# Check if the version number starts with "20."
if [[ $version == 20.* ]]; then

  apt update -y
  apt install -y gnupg

  # install remnux template
  
  cd /opt
  wget https://REMnux.org/remnux-cli
  chmod +x remnux-cli
  mv remnux-cli /usr/local/bin
  remnux-cli install --mode=cloud

  # install xrdp

  apt install xrdp -y
  passwd ubuntu
  
  reboot
  
else
  echo "This is not Ubuntu 20.xx."
fi
