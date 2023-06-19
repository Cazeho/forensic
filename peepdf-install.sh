#!/bin/bash

cd /opt
git clone https://github.com/jesparza/peepdf
cd peepdf
ln -s $PWD/peepdf.py /usr/local/bin/peepdf
