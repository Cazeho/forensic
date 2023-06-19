#!/usr/bin/python3

import imaplib
import email
import base64
import requests
import json

IMAP_SERVER = 'mtest.cazeho.ovh'
IMAP_USERNAME = 'user2'
IMAP_PASSWORD = 'root'



# Log in to the IMAP server and select the inbox folder
imap = imaplib.IMAP4_SSL(IMAP_SERVER)
imap.login(IMAP_USERNAME, IMAP_PASSWORD)
imap.select('inbox')

# Search for email messages with attachments
status, messages = imap.search(None, 'ALL')
messages = messages[0].split(b' ')
print(messages)

for message in messages:
    # Get the email message data
    status, msg_data = imap.fetch(message, '(RFC822)')
    email_data = msg_data[0][1]
    email_message = email.message_from_bytes(email_data)

    # Check if the message has attachments
    if email_message.get_content_maintype() != 'multipart':
        continue

attachment = email_message.get_payload()[1]
attachment_data = attachment.get_payload()
if attachment.get('Content-Transfer-Encoding') == 'base64':
attachment_data = base64.b64decode(attachment_data)


#print(attachment_data)

# VirusTotal Analysis


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
