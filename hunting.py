import requests
import json
import pandas as pd
import re

class Triage():
    def __init__(self, api: str):
        self.base_url = "https://tria.ge/api/v0/samples"
        self.api = api
        
        
    def result_report(self,id):
        url = f'{self.base_url}/{id}/overview.json'
        response = requests.get(url, headers=self.api)
        return response.json()

api_key_triage=""

def auth_triage(api_key):
    header = {'Authorization': 'Bearer ' + api_key}
    return header

triage=Triage(auth_triage(api_key_triage))
id="240513-qvyflsgg3z"
data=triage.result_report(id)
iocs_data = data['targets'][0]['iocs']

#print(iocs_data)

domains_df = pd.DataFrame(iocs_data['domains'], columns=['domain'])
ips_df = pd.DataFrame(iocs_data['ips'], columns=['ip'])
urls_df = pd.DataFrame(iocs_data['urls'], columns=['url'])

def extract_port(url):
    match = re.search(r':(\d+)', url)
    return match.group(1) if match else None


urls_df['port'] = urls_df['url'].apply(extract_port)


start_time = "2024-04-02 09:35:00 +0200"
end_time = "2024-04-02 09:42:00 +0200"
agent_hostname = "Cxxxxxxxx"


# Generate the XQL query
def generate_xql_query(domains, ips, start_time, end_time, agent_hostname):
    domain_filters = ' or '.join([f'dns_query_name = "*{domain}*"' for domain in domains])
    ip_filters = ' or '.join([f'dst_ip = "{ip}"' for ip in ips])
    
    filters = ' or '.join(filter(None, [domain_filters, ip_filters]))
    
    xql_query = f"""
    config timeframe between "{start_time}" and "{end_time}"
    | preset = network_story 
    | filter agent_hostname = "{agent_hostname}" and (dns_query_name != null and ({filters}))
    | dedup dns_query_name
    | fields _time, dns_query_name 
    | sort asc _time
    """
    return xql_query

# Extract values from DataFrames
domains_list = domains_df['domain'].tolist()
ips_list = ips_df['ip'].tolist()
urls_list = urls_df['url'].tolist()

# Generate XQL query
xql_query = generate_xql_query(domains_list, ips_list, start_time, end_time, agent_hostname)

print("Generated XQL Query:")
print(xql_query)

print("\nURLs DataFrame with Port:")
print(urls_df)
