#!/bin/bash

# ubuntu 20.04

# Get the version number of the current distribution
version=$(lsb_release -sr)

# Check if the version number starts with "20."
if [[ $version == 20.* ]]; then

  # install cast
  cd /usr/local/bin
  wget https://github.com/ekristen/cast/releases/download/v0.14.0/cast_v0.14.0_linux_amd64.deb
  dpkg -i cast_v0.14.0_linux_amd64.deb

  # install ubuntu-desktop

  apt install ubuntu-desktop


  # install sift template

  cast install teamdfir/sift-saltstack

  # install xrdp

  apt install xrdp
  passwd ubuntu
else
  echo "This is not Ubuntu 20.xx."
fi

