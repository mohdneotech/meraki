# title: Cisco Meraki Wireless Connected Clients Information Retrieval
# description: This script will retrieve connected clients information from Meraki wireless networks
#              within a network. The script will prompt for the Meraki API key and then
#              let the user choose an organization and network.
#              The script will then retrieve the connected clients information from the selected
#              Meraki wireless network and print the information in a table format.

import requests
from tabulate import tabulate
import pytz
from datetime import datetime  # Import the datetime module from the datetime library
import include.config as config

# Default API key (you can replace this with your default key)
DEFAULT_API_KEY = config.DEFAULT_API_KEY

# Meraki base URL
BASE_URL = config.BASE_URL

# Function to fetch organizations
def get_organizations(api_key):
    headers = {'X-Cisco-Meraki-API-Key': api_key}
    url = f'{BASE_URL}/organizations'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error fetching organizations: {e}')
        return None

# Function to fetch networks within an organization
def get_networks(api_key, org_id):
    headers = {'X-Cisco-Meraki-API-Key': api_key}
    url = f'{BASE_URL}/organizations/{org_id}/networks'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error fetching networks: {e}')
        return None

# Function to fetch connected clients in a network (without timespan)
def get_all_connected_clients(api_key, network_id):
    headers = {'X-Cisco-Meraki-API-Key': api_key}
    url = f'{BASE_URL}/networks/{network_id}/clients'

    all_clients = []

    while True:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            clients = response.json()
            all_clients.extend(clients)
            
            if 'Link' in response.headers:
                links = response.headers['Link'].split(',')
                for link in links:
                    if 'rel="next"' in link:
                        url = link.split(';')[0][1:-1]
                    else:
                        url = None
            else:
                url = None
            
            if not url:
                break
        except requests.exceptions.RequestException as e:
            print(f'Error fetching connected clients: {e}')
            break
    
    return all_clients

# Function to convert UTC time to GMT+8 (Singapore Time)
def convert_to_gmt_plus_8(utc_time_str):
    utc_time = datetime.strptime(utc_time_str, '%Y-%m-%dT%H:%M:%SZ')
    utc_time = pytz.utc.localize(utc_time)
    gmt_plus_8 = utc_time.astimezone(pytz.timezone('Asia/Singapore'))
    return gmt_plus_8.strftime('%Y-%m-%d %H:%M:%S GMT+8')

# Main function
def main():
    # Banner message
    print('Cisco Meraki Wireless Connected Clients Information Retrieval')
    print('Developer: Mohd NeoTech <mohdneotech@gmail.com>')
    print('-----------------------------------------------')    
    
    # Prompt for API key choice
    use_default_api_key = input('Do you want to use the default API key? (y/n): ').strip().lower()
    if use_default_api_key == 'y':
        api_key = DEFAULT_API_KEY
    else:
        api_key = input('Enter your Meraki API key: ')

    # Fetch organizations
    organizations = get_organizations(api_key)

    if organizations:
        # Display a list of organizations for the user to choose from
        print('Select an organization:')
        for i, org in enumerate(organizations, start=1):
            print(f'{i}. {org["name"]} ({org["id"]})')
        
        org_choice = int(input('Enter the number of the organization: '))
        if org_choice < 1 or org_choice > len(organizations):
            print('Invalid organization choice.')
            return
        
        selected_org = organizations[org_choice - 1]
        org_id = selected_org['id']

        # Fetch networks within the selected organization
        networks = get_networks(api_key, org_id)

        if networks:
            # Display a list of networks for the user to choose from
            print('Select a network:')
            for i, network in enumerate(networks, start=1):
                print(f'{i}. {network["name"]} ({network["id"]})')
            
            network_choice = int(input('Enter the number of the network: '))
            if network_choice < 1 or network_choice > len(networks):
                print('Invalid network choice.')
                return
            
            selected_network = networks[network_choice - 1]
            network_id = selected_network['id']

            # Fetch all connected clients without specifying a timespan
            connected_clients = get_all_connected_clients(api_key, network_id)

            if connected_clients:
                print(f'Total connected clients: {len(connected_clients)}')
                print('Connected Clients Details:')
                table = []
                for client in connected_clients:
                    last_seen_gmt_plus_8 = convert_to_gmt_plus_8(client.get("lastSeen", "N/A"))
                    table.append([
                        client.get("description", "N/A"),
                        client.get("mac", "N/A"),
                        client.get("ip", "N/A"),
                        client.get("userAgent", "N/A"),
                        client.get("vlan", "N/A"),
                        client.get("ssid", "N/A"),
                        last_seen_gmt_plus_8  # Display last seen time in GMT+8
                    ])
                
                headers = ["Client Name", "MAC Address", "IP Address", "User Agent", "VLAN", "Access Point", "Last Seen (GMT+8)"]
                print(tabulate(table, headers=headers, tablefmt="grid"))
            else:
                print('No connected clients found in the selected network.')
        else:
            print('No networks found in the selected organization.')
    else:
        print('No organizations found.')

if __name__ == '__main__':
    main()
