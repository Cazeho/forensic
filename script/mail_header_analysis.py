#!/usr/bin/python3


from email.parser import HeaderParser 
import imaplib
import email


IMAP_SERVER = 'mtest.cazeho.ovh'
IMAP_USERNAME = 'user1'
IMAP_PASSWORD = 'root'

# Log in to the IMAP server and select the inbox folder
imap = imaplib.IMAP4_SSL(IMAP_SERVER) 
imap.login(IMAP_USERNAME, IMAP_PASSWORD)
imap.select('inbox')

# Search for email messages with attachments
status, messages = imap.search(None, 'ALL') 
messages = messages[0].split(b' ')
print(messages)


def get_mail_header(msg):
    message_time = msg['Date']
    message_id = msg['Message-ID']
    sender_email = msg['From']
    recipient_email = msg['To']
    email_subject = msg['Subject']
    return_path = msg['Return-Path']
    x_originating_ip = msg['X-Originating-IP']
    sender_ip = msg['Received'].split()  # extract the sender's IP address from the "Received" header
    email_status = msg['X-Spam-Status']
    content_type=msg["Content-Type"]
    auth=msg["Authentication-Results-Original"]
    print(f"Message Time: {message_time}")
    print(f"Message ID: {message_id}")
    print(f"Sender's Email: {sender_email}")
    print(f"Recipient's Email: {recipient_email}")
    print(f"Email's Subject: {email_subject}")
    print(f"Return Path: {return_path}")
    print(f"X Originating IP: {x_originating_ip}")
    print(f"Sender's IP: {sender_ip}")
    print(f"Email's Status: {email_status}")
    print(f"Email's content-type: {content_type}")
    print(f"Email's Auth: {auth}")
    print("Receive: ",msg["Received"])
    print("Return path:", msg["Return-Path"])






for message in messages:
    # Get the email message data
    status, msg_data = imap.fetch(message, '(RFC822)')
    email_data = msg_data[0][1]
    email_message = email.message_from_bytes(email_data)
    msg=HeaderParser().parsestr(str(email_message))
    get_mail_header(msg)
