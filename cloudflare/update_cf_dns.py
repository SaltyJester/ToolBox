#!/usr/bin/env python3

import sys
import requests
import socket

WAN_CHECK_URL = 'https://api.ipify.org/'
DNS_RECORD_NAME = ''
API_TOKEN = ''
EMAIL = ''
ZONE_ID = ''
RECORD_ID = ''
API_URL= f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{RECORD_ID}'

# Get WAN IP
def get_wan_ip():
    try:
        response = requests.get('https://api.ipify.org/')
        if response.status_code == 200:
            return response.text
        else:
            print(f'Failed to retrieve WAN IP: Status Code, {response.status_code}')
            sys.exit(1)
    except Exception as e:
        print("Error with get_want_ip:", e)
        sys.exit(1)

# Get DNS Record IP
def get_hostname_ip(api_token):
    try:
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
        }

        response = requests.get(API_URL, headers=headers)
        if(response.status_code == 200):
            data = response.json()
            return data['result']['content']
        else:
            print(f'Failed to get DNS Record: Status Code: {response.status_code}')
            sys.exit(1)
        
    except requests.RequestException as e:
        print(f'Error with get_hostname_ip(): {e}')
        sys.exit(1)

# Update DNS Record
def update_dns_record(hostname, wan_ip, api_token):
    try:
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
        }

        data = {
        'type': 'A',  # Type of DNS record (A, CNAME, MX, etc.)
        'name': hostname,
        'content': wan_ip,
        'ttl': 60,  # TTL (Time To Live) in seconds
        }

        response = requests.put(API_URL, headers=headers, json=data)
        if(response.status_code == 200):
            print(f'{hostname} was updated to {wan_ip}')
        else:
            print(f'Failed to update DNS Record: Status Code: {response.status_code}')
            sys.exit(1)
    except requests.RequestException as e:
        print(f'Error with update_dns_record(): {e}')
        sys.exit(1)


# Main
wan_ip = get_wan_ip()
print(f'The WAN IP is {wan_ip}')

hostname_ip = get_hostname_ip(API_TOKEN)
print(f'The IP of {DNS_RECORD_NAME} is: {hostname_ip}')

if(wan_ip != hostname_ip):
    update_dns_record(DNS_RECORD_NAME, wan_ip, API_TOKEN)
else:
    print(f'DNS record IP already matches WAN IP')

sys.exit(0)