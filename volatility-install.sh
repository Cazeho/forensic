#!/bin/bash

apt install python2 python2.7-dev libpython2-dev -y
apt install python-pip -y
apt install subversion -y

pip2 install pycrypto
pip2 install distorm3

cd /usr/local/lib/python2.7/dist-packages/

svn export https://github.com/volatilityfoundation/volatility/trunk/volatility

mkdir -p /opt/volatility
cd /opt/volatility
chmod +x vol.py

ln -s $PWD/vol.py /usr/local/bin/volatility


## add firefox plugins & other

cd /usr/local/lib/python2.7/dist-packages/volatility/trunk/volatility/plugins/

git clone https://github.com/superponible/volatility-plugins.git
cd volatility-plugins
mv * ..
cd ..
rm -rf volatility-plugins

## hollowfind

git clone https://github.com/monnappa22/HollowFind.git
cd HollowFind
mv * ..
cd ..
rm -rf HollowFind



