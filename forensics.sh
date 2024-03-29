#!/bin/bash

# install volatility
curl -s https://raw.githubusercontent.com/Cazeho/forensic/main/volatility-install.sh | sh

# install peepdf
curl -s https://raw.githubusercontent.com/Cazeho/forensic/main/peepdf-install.sh | sh

# install extract tools

apt install binutils -y
apt install foremost -y
apt install pdftk -y
apt install nodejs -y
apt install hashcat -y
apt install snapd -y
snap install john-the-ripper -y

pip install dissect
pip install oletools
pip2 install -U balbuzard
pip install LnkParse3


# john-the-ripper --format=NT -w=dict.txt hash.txt
# john-the-ripper --format=NT  hash.txt --show
