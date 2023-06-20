#!/bin/bash

# install volatility
curl -s https://raw.githubusercontent.com/Cazeho/forensic/main/volatility-install.sh | sh

# install peepdf
curl -s https://raw.githubusercontent.com/Cazeho/forensic/main/peepdf-install.sh | sh

# install extract tools

apt install foremost -y
apt install pdftk -y
apt install nodejs -y
apt install hashcat -y
