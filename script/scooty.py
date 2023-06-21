"""
Scooty

Usage:

scooty <file_path> --show
scooty --hash <file_path> --show
scooty <file_path> --send
scooty --hash (md5|sha256) <file_path> --send
scooty --hash (md5|sha256) <file_path>
"""
#! /usr/bin/python3

import requests
import json
import hashlib
import argparse

import sys


BUF_SIZE = 128536
md5 = hashlib.md5()
sha256 = hashlib.sha256()

def get_hash(file):
    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
            sha256.update(data)


def hash():
    pass






## VT

data={}

VT_API_ENDPOINT = 'https://www.virustotal.com/api/v3/files'

session = requests.Session()
session.headers = {'X-Apikey': '7b6e2f3c3a8067581502a841b1a06346772e12c263d49a41e60f948a5b83d6cb'}

class scooty:

    def send_file(self):
        attachment_data = open(sys.argv[1],'rb')#.read()
        files = {'file': (sys.argv[1], attachment_data)}
        response = requests.post(VT_API_ENDPOINT, files=files,headers=session.headers)
        scan_id = response.json()['data']['id']
        VT_API_REPORT_ENDPOINT = f'https://www.virustotal.com/api/v3/analyses/{scan_id}'
        response = requests.get(VT_API_REPORT_ENDPOINT, headers=session.headers)
        res=response.json()["url"]=f"https://www.virustotal.com/gui/file/{response.json()['meta']['file_info']['sha256']}"
        data["analyse"]=response.json()
        data["link"]=res
        return data

    
    def send_hash(self):
        get_hash(sys.argv[1])
        hash=sha256.hexdigest()
        #hash=md5.hexdigest()
        #hash="b2a96537b627cc5f7ed63b4b9491b9ea15b08c88dfdd5aeb7a00d903dd4d0176"
        VT_API_SEARCH_HASH=f'https://www.virustotal.com/api/v3/search?query={hash}'
        response = session.get(VT_API_SEARCH_HASH)
        if response.status_code == 200 and len(response.json()['data']) > 0:
            return response.json()
        else:
            #return "no match found"
            return hash

scooty=scooty()

print(scooty.send_file())
#print(scooty.send_hash())




