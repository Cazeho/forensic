#!/bin/bash

apt install python2 python2.7-dev libpython2-dev -y
apt install python-pip
apt install subversion

pip2 install pycrypto
pip2 install distorm3

cd /usr/local/lib/python2.7/dist-packages/

svn export https://github.com/volatilityfoundation/volatility/trunk/volatility

mkdir -p /opt/volatility
cd /opt/volatility
chmod +x vol.py

ln -s $PWD/vol.py /usr/local/bin/volatility


## add firefox plugins & other
