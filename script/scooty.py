"""
Scooty

Usage:

scooty <file_path> --show
scooty --hash <file_path> --show
scooty <file_path> --send
scooty --hash (md5|sha256) <file_path> --send
scooty --hash (md5|sha256) <file_path>
"""

import requests
import json
import hashlib
import argparse

### VT

## send hash

session = requests.Session()
session.headers = {'X-Apikey': '7b6e2f3c3a8067581502a841b1a06346772e12c263d49a41e60f948a5b83d6cb'}

url = "https://www.virustotal.com/api/v3/search?query=b2a96537b627cc5f7ed63b4b9491b9ea15b08c88dfdd5aeb7a00d903dd4d0176"
response = session.get(url)
print(response.text)


## send file

VT_API_ENDPOINT = 'https://www.virustotal.com/api/v3/files'
VT_API_KEY = '7b6e2f3c3a8067581502a841b1a06346772e12c263d49a41e60f948a5b83d6cb'

headers = {
    'x-apikey': VT_API_KEY,
    "accept": "application/json"
}


files = {'file': ('attachment', attachment_data)}
# Send the file to VirusTotal for scanning
response = requests.post(VT_API_ENDPOINT, files=files, headers=headers)
# Get the scan ID from the response
scan_id = response.json()['data']['id']

VT_API_REPORT_ENDPOINT = f'https://www.virustotal.com/api/v3/analyses/{scan_id}'

print(VT_API_REPORT_ENDPOINT)
response = requests.get(VT_API_REPORT_ENDPOINT, headers=headers)

print(response.json())
